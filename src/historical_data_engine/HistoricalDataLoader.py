import pandas as pd

from historical_data_engine.source.AbstractDataSource import AbstractDataSource
from historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from historical_data_engine.request.AbstractRequestSettings import RequestSettings


class HistoricalDataLoader:
    def __init__(self, data_source: AbstractDataSource):
        self._data_source = data_source

    def load_historical_data(
            self,
            instrument: InstrumentSettings,
            request: RequestSettings
    ) -> pd.DataFrame:
        result = self._data_source.fetch_historical_data(instrument, request)
        return result