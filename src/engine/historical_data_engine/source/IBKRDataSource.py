import pandas as pd

from engine.historical_data_engine.Errors import TWSConnectionError
from engine.historical_data_engine.source.AbstractDataSource import AbstractDataSource
from engine.historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from engine.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings

from engine.historical_data_engine.connection.TWSConnection import TWSConnection
from engine.historical_data_engine.HistoricalRequestBuilder import HistoricalRequestBuilder
from engine.utilities.logger.protocol import LoggerProtocol


class IBKRDataSource(AbstractDataSource):

    def __init__(
            self,
            logger: LoggerProtocol,
            connection: TWSConnection
    ):
        self._logger = logger
        self._tws_connection = connection

    def fetch_historical_data(
            self,
            instrument: InstrumentSettings,
            request: IBKRRequestSettings
    ) -> pd.DataFrame:
        query = HistoricalRequestBuilder.build(instrument, request)
        self._logger.info("Requesting Historical data...")
        try:
            result = self._tws_connection.ib.reqHistoricalData(**query)
            self._logger.info("Historical data request successful.")
        except Exception as e:
            raise TWSConnectionError(f"Failed to request data from IBKR: {e}") from e
        df = pd.DataFrame(result)
        return df

    def connect(self) -> None:
        self._tws_connection.connect()

    def disconnect(self) -> None:
        self._tws_connection.disconnect()