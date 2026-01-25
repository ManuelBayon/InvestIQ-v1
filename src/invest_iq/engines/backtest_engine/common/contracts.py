from dataclasses import dataclass, field

from invest_iq.common.market_types import MarketEvent
from invest_iq.engines.backtest_engine.common.enums import FIFOSide
from invest_iq.engines.backtest_engine.common.types import ExecutionLogEntry, FIFOPosition
from invest_iq.engines.strategy_engine.contracts import OrchestratorOutput, StrategyOutput, FilterOutput

@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    asset_class: str        # "FUT", "EQ", "FX", ...
    bar_size: str           # "1 min", "5 min", ...
    timezone: str | None = None

@dataclass(frozen=True)
class BacktestInput:
    instrument: InstrumentSpec
    events: list[MarketEvent]

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
    fifo_queues: dict[FIFOSide, list[FIFOPosition]] = field(default_factory=dict)
    execution_log: list[ExecutionLogEntry] = field(default_factory=list)


@dataclass
class BacktestResult:
    execution_log: list[ExecutionLogEntry]
    final_cash: float
    realized_pnl: float
    unrealized_pnl: float
    diagnostics: dict[str, dict[str, float]] = field(default_factory=dict)
