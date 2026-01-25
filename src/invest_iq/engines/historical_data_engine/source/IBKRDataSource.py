import pandas as pd

from invest_iq.engines.historical_data_engine.Errors import TWSConnectionError
from invest_iq.engines.historical_data_engine.source.AbstractDataSource import AbstractDataSource
from invest_iq.engines.historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from invest_iq.engines.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings

from invest_iq.engines.historical_data_engine.connection.TWSConnection import TWSConnection
from invest_iq.engines.historical_data_engine.HistoricalRequestBuilder import HistoricalRequestBuilder
from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


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