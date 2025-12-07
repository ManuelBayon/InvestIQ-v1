from abc import ABC, abstractmethod

import pandas as pd


class BaseFilter(ABC):

    @abstractmethod
    def apply_filter(self, data: pd.DataFrame) -> pd.DataFrame:
        ...