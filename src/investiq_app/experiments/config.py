from dataclasses import dataclass

from investiq.api.filter import Filter
from investiq.api.instruments import AssetClass
from investiq.api.strategy import Strategy
from investiq.data.historical_data_engine.enums import BarSize


@dataclass
class BacktestConfig:
    symbol: str
    asset_class: AssetClass
    duration_setting : str
    bar_size_setting : BarSize
    strategy : Strategy
    filters : list[Filter] | None
    initial_cash : int