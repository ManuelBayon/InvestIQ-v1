from dataclasses import dataclass

from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.historical_data_engine.enums import BarSize
from invest_iq.engines.strategy_engine.filters.abstract_filter import AbstractFilter
from invest_iq.engines.strategy_engine.strategies.abstract_strategy import AbstractStrategy


@dataclass
class BacktestConfig:
    symbol: str
    asset_class: str
    duration_setting : str
    bar_size_setting : BarSize
    strategy : AbstractStrategy
    filters : list[AbstractFilter] | None
    initial_cash : int