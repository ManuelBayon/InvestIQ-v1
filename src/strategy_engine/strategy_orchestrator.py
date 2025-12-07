import pandas as pd

from strategy_engine.AbstractStrategy import AbstractStrategy
from strategy_engine.filters.base_filter import BaseFilter


class StrategyOrchestrator:

    def __init__(self, strategy: AbstractStrategy):
        self.strategy: AbstractStrategy = strategy
        self.filters: list[BaseFilter] = []

    def add_filter(self, filter_: BaseFilter):
        self.filters.append(filter_)

    def run(self, data: pd.DataFrame) -> pd.DataFrame:

        df = self.strategy.generate_raw_signals(data)

        for f in self.filters:
            df = f.apply_filter(df)

        df["timestamp"] = df["date"]
        return df[["timestamp", "close", "target_position"]]
