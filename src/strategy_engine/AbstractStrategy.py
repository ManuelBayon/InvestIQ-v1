from abc import ABC, abstractmethod

import pandas as pd


class AbstractStrategy(ABC):


    @abstractmethod
    def generate_raw_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass