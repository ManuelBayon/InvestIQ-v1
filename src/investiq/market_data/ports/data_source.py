from abc import ABC, abstractmethod
import pandas as pd

from investiq.market_data.domain.instruments.base import InstrumentSpec
from investiq.market_data.domain.requests.base import RequestSpec


class HistoricalDataSource(ABC):

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def fetch_historical_data(
        self,
        instrument: InstrumentSpec,
        request: RequestSpec,
    ) -> pd.DataFrame:
        ...