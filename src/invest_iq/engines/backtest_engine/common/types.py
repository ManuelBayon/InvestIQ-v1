from datetime import datetime
from typing import Optional, Any

import pandas as pd

from collections.abc import Sequence, Mapping, Iterable
from dataclasses import dataclass, field

from invest_iq.engines.backtest_engine.common.errors import ContextNotInitializedError
from invest_iq.engines.historical_data_engine.enums import BarSize
from invest_iq.engines.strategy_engine.enums import MarketField
from invest_iq.engines.strategy_engine.strategies.metadata import StrategyMetadata
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, CurrentState, Event, FIFOOperationType, FIFOSide

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
    strategy_name: str
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

@dataclass
class BacktestResultExport:
    strategy_name: str
    run_id: str
    instrument: str
    metrics: dict[str, float]
    execution_log: list[ExecutionLogEntry]
    transition_log: list[TransitionLog]
    parameters: dict[str, Any]
    start: datetime
    end: datetime

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
class StrategyInput:
    timestamp: pd.Timestamp
    bar: OHLCV
    history: Mapping[str, Sequence[float]]


@dataclass(frozen=True)
class FilterInput:
    timestamp: pd.Timestamp
    raw_target: float
    features: dict[str, object] | None = field(default_factory=dict)


@dataclass(frozen=True)
class StrategyOutput:
    timestamp: pd.Timestamp
    raw_target: float
    price: float
    price_type: MarketField
    metadata: StrategyMetadata
    diagnostics: dict[str, object] | None = field(default_factory=dict)


@dataclass(frozen=True)
class FilterOutput:
    timestamp: pd.Timestamp
    target_position: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)


@dataclass(frozen=True)
class OrchestratorOutput:
    timestamp: pd.Timestamp
    target_position: float
    price_type: MarketField
    price: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)


@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    asset_class: str  # "FUT", "EQ", "FX", ...
    bar_size: BarSize  # "1 min", "5 min", ...
    timezone: str | None = None


@dataclass(frozen=True)
class BacktestInput:
    instrument: InstrumentSpec
    events: Iterable[MarketEvent]


@dataclass(frozen=True)
class ModelState:
    strategy: StrategyOutput | None = None
    filtered: FilterOutput | None = None
    orchestrator: OrchestratorOutput | None = None


@dataclass(frozen=True)
class ExecutionState:
    current_position: float = 0.0
    cash: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    fifo_queues: dict[FIFOSide, list[FIFOPosition]] = field(default_factory=dict)
    execution_log: list[ExecutionLogEntry] = field(default_factory=list)


@dataclass(frozen=True)
class MarketState:
    snapshot: MarketEvent | None = None
    series: dict[str, list[float]] = field(default_factory=dict)


@dataclass(frozen=True)
class FeatureState:
    computed: dict[str, float] = field(default_factory=dict)
    history: dict[str, list[float]] = field(default_factory=dict)


@dataclass(frozen=True)
class BacktestState:
    model: ModelState = field(default_factory=ModelState)
    execution: ExecutionState = field(default_factory=ExecutionState)
    market: MarketState = field(default_factory=MarketState)
    features: FeatureState = field(default_factory=FeatureState)

    @property
    def timestamp(self) -> pd.Timestamp:
        if self.market.snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        return self.market.snapshot.timestamp

    @property
    def bar(self) -> OHLCV:
        if self.market.snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        return self.market.snapshot.bar


@dataclass
class BacktestResult:
    execution_log: list[ExecutionLogEntry]
    final_cash: float
    realized_pnl: float
    unrealized_pnl: float
    diagnostics: dict[str, dict[str, float]] = field(default_factory=dict)

@dataclass(frozen=True)
class MarketView:
    snapshot: MarketEvent
    history: Mapping[str, Sequence[float]]

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

@dataclass(frozen=True)
class StepRecord:
    timestamp: pd.Timestamp
    event: MarketEvent
    orchestrator_output: OrchestratorOutput
    transition_result: list[FIFOOperation]
    execution_after: ExecutionView
    diagnostics: Mapping[str, object]

class MarketStore:
    def __init__(self):
        self._snapshot: MarketEvent | None = None
        self._history: dict[str, list[float]] = {}

    def ingest(self, event: MarketEvent) -> None:
        self._snapshot = event
        for k, v in event.bar.items():
            self._history.setdefault(k, []).append(v)

    def view(self) -> MarketView:
        if self._snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        return MarketView(
            snapshot=self._snapshot,
            history=self._history,
        )

