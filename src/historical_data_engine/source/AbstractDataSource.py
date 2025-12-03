from abc import ABC, abstractmethod

import pandas as pd

from historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from historical_data_engine.request.AbstractRequestSettings import RequestSettings


class AbstractDataSource(ABC):
    @abstractmethod
    def fetch_historical_data(
            self,
            instrument: InstrumentSettings,
            request: RequestSettings
    ) -> pd.DataFrame:
        pass
    @abstractmethod
    def connect(self) -> None:...

    @abstractmethod
    def disconnect(self) -> None: ...