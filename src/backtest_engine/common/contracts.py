from dataclasses import dataclass, field

import pandas as pd

from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import ExecutionLogEntry, FIFOOperation, FIFOPosition
from strategy_engine.contracts import OrchestratorOutput, StrategyOutput, FilterOutput


@dataclass(frozen=True)
class BacktestInput:
    timestamp: pd.Series
    data: dict[str, pd.Series]

@dataclass
class ModelState:
    strategy: StrategyOutput | None = None
    filtered: FilterOutput | None = None
    orchestrator: OrchestratorOutput | None = None

@dataclass
class ExecutionState:
    current_position: float = 0.0
    cash: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    fifo_queues: dict[FIFOSide, list[FIFOPosition]] = field(default_factory=list)
    execution_log: list[ExecutionLogEntry] = field(default_factory=list)

@dataclass
class BacktestContext:
    timestamp: pd.Timestamp
    bar: dict[str, float]
    history: dict[str, list[float]]

    model: ModelState
    execution: ExecutionState

    features: dict[str, float] = field(default_factory=dict)
    features_history: dict[str, list[float]] = field(default_factory=dict)


@dataclass
class BacktestResult:
    context: BacktestContext
    summary: dict[str, object] = None
