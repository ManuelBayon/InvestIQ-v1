from dataclasses import dataclass, field

import pandas as pd

from backtest_engine.common.types import ExecutionLogEntry, FIFOOperation, FIFOPosition
from strategy_engine.strategies.contracts import OrchestratorOutput, StrategyOutput, FilterOutput


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
    fifo_positions : list[FIFOPosition] = field(default_factory=list)
    fifo_operations: list[FIFOOperation] = field(default_factory=list)
    execution_log: list[ExecutionLogEntry] = field(default_factory=list)
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0

@dataclass
class BacktestContext:
    timestamp: pd.Timestamp
    bar: dict[str, float]
    history: dict[str, list[float]]

    model: ModelState
    execution: ExecutionState


@dataclass
class BacktestResult:
    context: BacktestContext
    summary: dict[str, object] = None
