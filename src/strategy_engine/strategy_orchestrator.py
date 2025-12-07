import pandas as pd

from strategy_engine.strategies.abstract_strategy import AbstractStrategy
from strategy_engine.filters.base_filter import BaseFilter
from strategy_engine.strategies.contracts import StrategyInput
from utilities.timestamps import timestamp_with_timezone, unify_timestamp_column


class StrategyOrchestrator:

    def __init__(self, strategy: AbstractStrategy):
        self.strategy: AbstractStrategy = strategy
        self.filters: list[BaseFilter] = []

    def add_filter(self, filter_: BaseFilter):
        self.filters.append(filter_)

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        df = unify_timestamp_column(data)
        df = timestamp_with_timezone(df=df)
        inp = StrategyInput(
            timestamp=df["timestamp"],
            close=df["close"],
            extra = {

            }
        )
        df = self.strategy.generate_raw_signals(inp)
        df.to_excel("raw_signals.xlsx")
        for f in self.filters:
            df = f.apply_filter(df)
        df.to_excel("filtered_signals.xlsx")
        return df[["timestamp", "close", "target_position"]]