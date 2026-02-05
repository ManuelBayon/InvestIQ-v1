from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Optional, Any

import pandas as pd

from collections.abc import Sequence, Mapping, Iterable
from dataclasses import dataclass, field

from invest_iq.engines.backtest_engine.common.errors import ContextNotInitializedError
from invest_iq.engines.historical_data_engine.enums import BarSize
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, CurrentState, Event, FIFOOperationType, FIFOSide

class Version(StrEnum):
    V1= "1.0"

class ComponentType(StrEnum):
    STRATEGY = "strategy"
    FILTER = "filter"

class MarketField(StrEnum):
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"

class AssetClass(StrEnum):
    CONT_FUT = "CONT_FUT"

@dataclass(frozen=True)
class AtomicAction:
    type : AtomicActionType
    quantity : float
    timestamp: datetime

@dataclass(frozen=True)
class TransitionLog:
    state: CurrentState
    event: Event
    current_position: float
    target_position: float
    rule_name: str
    transition_strategy: str
    transition_type: str
    actions_len: int
    fifo_ops_len: int

@dataclass(frozen=True)
class ExecutionLogEntry:
    timestamp: datetime
    operation_type : FIFOOperationType
    side : FIFOSide
    quantity : float
    entry_price : float
    pos_before : float
    pos_after: float
    exit_price: Optional[float] = None
    realized_pnl: Optional[float] = None
    parent_id : Optional[int] = None

@dataclass
class FIFOPosition:
    id : int
    is_active : bool
    timestamp : datetime
    type : FIFOOperationType
    side : FIFOSide
    quantity : float
    price : float

    _next_id = 0

    @classmethod
    def next_id(cls) -> int:
        id_ = cls._next_id
        cls._next_id += 1
        return id_

@dataclass
class FIFOOperation:
    id : int
    timestamp : datetime
    type : FIFOOperationType
    side : FIFOSide
    execution_price : float
    quantity : float
    linked_position_id: Optional[int] = None

    _next_id = 0

    @classmethod
    def next_id(cls) -> int:
        id_ = cls._next_id
        cls._next_id += 1
        return id_

@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    asset_class: str  # "FUT", "EQ", "FX", ...
    bar_size: BarSize  # "1 min", "5 min", ...
    timezone: str | None = None

@dataclass(frozen=True)
class RunResult:
    run_id: str
    instrument: InstrumentSpec
    start: pd.Timestamp
    end: pd.Timestamp
    metrics: Mapping[str, float]
    execution_log: list[ExecutionLogEntry]
    transition_log: list[TransitionLog] = field(default_factory=tuple)
    diagnostics: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ResolveContext:
    """
    Unchanging context passed to SafeGuards strategies.
    Combines action, fifo status, and execution price for deterministic checks
    with no side effects.
    """
    action: AtomicAction
    fifo_queues: dict[FIFOSide, list[FIFOPosition]]
    execution_price: float


@dataclass(frozen=True)
class OHLCV:
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def __getitem__(
            self,
            key: str
    ) -> float:
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(key) from e

    def __contains__(
            self,
            key: object
    ) -> bool:
        return isinstance(key, str) and hasattr(self, key)

    def items(self):
        for k in (
                "open",
                "high",
                "low",
                "close",
                "volume"
        ):
            yield k, getattr(self, k)


@dataclass(frozen=True)
class MarketEvent:
    timestamp: pd.Timestamp
    bar: OHLCV
    symbol: str | None = None
    bar_size: str | None = None

@dataclass(frozen=True)
class Decision:
    timestamp: pd.Timestamp
    target_position: float
    execution_price: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)

@dataclass(frozen=True)
class BacktestInput:
    instrument: InstrumentSpec
    events: Iterable[MarketEvent]

@dataclass(frozen=True)
class MarketView:
    snapshot: MarketEvent
    history: Mapping[MarketField, Sequence[float]]
    @property
    def timestamp(self) -> pd.Timestamp:
        return self.snapshot.timestamp
    @property
    def bar(self) -> OHLCV:
        return self.snapshot.bar

@dataclass(frozen=True)
class ExecutionView:
    current_position: float
    cash: float
    realized_pnl: float
    unrealized_pnl: float

@dataclass(frozen=True)
class BacktestView:
    """
    The ONLY object passed to strategies/orchestrator.
    Read-only contract: strategies cannot mutate the world.
    """
    market: MarketView
    execution: ExecutionView

class MarketStore:

    def __init__(self):
        self._snapshot: MarketEvent | None = None
        self._history: dict[MarketField, list[float]] = {}

    def ingest(self, event: MarketEvent) -> None:
        self._snapshot = event
        for k, v in event.bar.items():
            self._history.setdefault(MarketField(k), []).append(v)

    def view(self) -> MarketView:
        if self._snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        # freeze lists into tuples (no accidental mutation)
        frozen = {k: tuple(v) for k, v in self._history.items()}
        return MarketView(
            snapshot=self._snapshot,
            history=MappingProxyType(frozen),
        )

@dataclass(frozen=True)
class StepRecord:
    timestamp: pd.Timestamp
    event: MarketEvent
    decision: Decision
    transition_result: list[FIFOOperation]
    execution_after: ExecutionView
    diagnostics: Mapping[str, object]