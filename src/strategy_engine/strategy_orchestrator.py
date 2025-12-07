from abc import ABC, abstractmethod

import pandas as pd

from strategy_engine.AbstractStrategy import AbstractStrategy


class BaseStrategy(AbstractStrategy):

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        ...