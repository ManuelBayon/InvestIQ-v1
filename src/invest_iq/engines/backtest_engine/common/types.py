from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

import pandas as pd

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

