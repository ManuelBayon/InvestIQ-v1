from abc import ABC, abstractmethod

import pandas as pd


class AbstractStrategy(ABC):

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass