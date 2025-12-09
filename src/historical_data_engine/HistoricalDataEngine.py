import pandas as pd

from historical_data_engine.source.AbstractDataSource import AbstractDataSource
from historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from historical_data_engine.request.AbstractRequestSettings import RequestSettings
from historical_data_engine.HistoricalDataLoader import HistoricalDataLoader
from utilities.logger.protocol import LoggerProtocol


class HistoricalDataEngine:
    def __init__(
        self,
        logger: LoggerProtocol,
        instrument_settings: InstrumentSettings,
        request_settings: RequestSettings,
        data_source: AbstractDataSource
    ):
        self._logger = logger
        self.instrument = instrument_settings
        self.request = request_settings
        self._data_source = data_source

    def load_data(self) -> pd.DataFrame:
        self._logger.info("Initializing historical data engine...")
        self._data_source.connect()
        self._logger.info(" Historical data engine initialized successfully.")
        loader = HistoricalDataLoader(self._data_source)
        data = loader.load_historical_data(self.instrument, self.request)
        df = pd.DataFrame(data)
        self._data_source.disconnect()
        if "date" in df.columns:
            df = df.rename(columns={"date": "timestamp"})
        return df