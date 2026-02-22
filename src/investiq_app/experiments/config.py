from dataclasses import dataclass

from investiq.api.filter import Filter
from investiq.api.instruments import AssetClass
from investiq.api.strategy import Strategy
from investiq.core.execution_planner import ExecutionPlanner
from investiq.market_data import BarSize


@dataclass
class BacktestConfig:
    debug: bool
    symbol: str
    asset_class: AssetClass
    duration_setting : str
    bar_size_setting : BarSize
    strategy : Strategy
    execution_planner: ExecutionPlanner
    filters : list[Filter] | None
    initial_cash : int