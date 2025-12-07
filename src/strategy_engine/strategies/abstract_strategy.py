from abc import ABC, abstractmethod

import pandas as pd

from strategy_engine.strategies.contracts import StrategyInput


class AbstractStrategy(ABC):
    @abstractmethod
    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> pd.DataFrame:
        pass