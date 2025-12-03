from historical_data_engine.Errors import TWSConnectionError
from historical_data_engine.connection.ConnectionConfig import ConnectionConfig
from ib_insync import IB

from utilities.logger.factory import LoggerFactory
from utilities.logger.protocol import LoggerProtocol


class TWSConnection:

    def __init__(
            self,
            logger : LoggerProtocol,
            connection_config : ConnectionConfig = ConnectionConfig.paper()
    ):
        self._logger = logger
        self._ib: IB= IB()
        self._connection_config = connection_config
        self._connected = False


    # ---------------- START - FUNCTION - Connect to IBKR ----------------
    def connect(self) -> None:
        if self._connected:
            self._handle_already_connected()
        try:
            self._log_connecting()
            self._perform_connection()
            self._validate_connection()
            self._connected = True
            self._log_connected()
        except Exception as e:
            self._logger.error(f"Failed to connect to IB - {e}")
            raise TWSConnectionError(f"Failed to connect to IB - {e}")

    def _handle_already_connected(self) -> bool:
        self._logger.error('Already connected to IB')
        raise TWSConnectionError('Already connected to IB')

    def _log_connecting(self) -> None:
        self._logger.info('Connecting to IB...')

    def _perform_connection(self) -> None:
        self._ib.connect(
            host=self._connection_config.host,
            port=self._connection_config.port,
            clientId=self._connection_config.client_id
        )

    def _validate_connection(self) -> None:
        if not self._ib.isConnected():
            raise TWSConnectionError("Connection to IB failed")

    def  _log_connected(self) -> None:
       self._logger.info('Connected to IB')

    # ---------------- END - FUNCTION - Connect to IBKR ----------------

    # ---------------- START - FUNCTION - Disconnect from IBKR ----------------

    def disconnect(self) -> None:
        if not self._connected:
            self._handle_no_active_connection()
        try:
            self._log_disconnecting()
            self._perform_disconnection()
            self._validate_disconnection()
            self._connected = False
            self._log_disconnected()
        except Exception as e:
            self._logger.error(f"An error occurred during the disconnection process : {e}")
            raise TWSConnectionError(f'An error occurred during the disconnection process : {e}') from e

    def _handle_no_active_connection(self) -> None:
        self._logger.error('No active connection found from IB')
        raise TWSConnectionError('No active connection found from IB')

    def _log_disconnecting(self) -> None:
        self._logger.info('Disconnecting from IB...')

    def _perform_disconnection(self) -> None:
        self._ib.disconnect()

    def _validate_disconnection(self) -> None:
        if self._ib.isConnected():
            raise TWSConnectionError('Disconnection from IB failed')

    def _log_disconnected(self) -> None:
        self._logger.info('Disconnected from IB')

    # ---------------- END - FUNCTION - Disconnect from IBKR ----------------

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def ib(self):
        return self._ib

    def __repr__(self):
        mode = self._connection_config.mode.name
        return f'TWSConnection(connected={self._connected}, mode={mode})'

    def __enter__(self) -> "TWSConnection":
        self.connect()
        return self

    def __exit__(self, exc_type:BaseException, exc_val, exc_tb) -> None:
        try:
            self.disconnect()
        except Exception as e:
            self._logger.error(f'Failed to disconnect from TWS {e}')
            raise TWSConnectionError(f'Failed to disconnect from TWS {e}') from e
