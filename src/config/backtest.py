from dataclasses import dataclass

from engine.backtest_engine.common.enums import FutureCME
from engine.historical_data_engine.enums import BarSize
from engine.strategy_engine.filters.abstract_filter import AbstractFilter
from engine.strategy_engine.strategies.abstract_strategy import AbstractStrategy


@dataclass
class BacktestConfig:
    symbol: FutureCME
    duration_setting : str
    bar_size_setting : BarSize
    strategy : AbstractStrategy
    filters : list[AbstractFilter] | None
    initial_cash : int