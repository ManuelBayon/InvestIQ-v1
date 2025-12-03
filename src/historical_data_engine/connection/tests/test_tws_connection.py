from unittest.mock import MagicMock
import pytest

from historical_data_engine.Errors import TWSConnectionError
from historical_data_engine.connection.TWSConnection import TWSConnection
from historical_data_engine.connection.ConnectionConfig import ConnectionConfig

@pytest.fixture
def fake_connection_config():
    return ConnectionConfig.paper()

@pytest.fixture
def connection(test_logger_factory, fake_connection_config):
    conn = TWSConnection(logger=test_logger_factory, connection_config=fake_connection_config)
    conn._ib = MagicMock()  # On mock IB
    return conn

def test_connect_successful_flow(mocker, connection, caplog):
    # Initialisation
    mocker.patch.object(connection, "_perform_connection")
    connection._ib.isConnected.return_value = True
    # Start test
    with caplog.at_level("INFO"):
        connection.connect()
    # Assertions for test validation
    assert connection.connected is True
    assert any (record.levelname == "INFO" for record in caplog.records)
    assert not any(record.levelname == "ERROR" for record in caplog.records)

def test_connect_unsuccessful_flow(mocker, connection, caplog):
    # Initialisation
    mocker.patch.object(connection, "_perform_connection")
    connection._ib.isConnected.return_value = False
    # Start test
    with caplog.at_level("ERROR"), pytest.raises(TWSConnectionError):
        connection.connect()
    # Assertions for test validation
    assert any(record.levelname == "ERROR" for record in caplog.records)

def test_connect_with_active_connection(connection, caplog):
    # Initialisation
    connection._connected = True
    # Start the test
    with caplog.at_level("ERROR"), pytest.raises(TWSConnectionError):
        connection.connect()
    # Assertions for test validation
    assert any(record.levelname == "ERROR" for record in caplog.records)

def test_disconnect_successful_flow(mocker, connection, caplog):
    # Initialisation
    mocker.patch.object(connection, "_perform_disconnection")
    connection._connected = True
    connection._ib.isConnected.return_value = False
    # Start the test
    with caplog.at_level("INFO"):
        connection.disconnect()
    # Assertions for test validation
    assert connection._connected is False
    assert any(record.levelname == "INFO" for record in caplog.records)
    assert not any(record.levelname == "ERROR" for record in caplog.records)

def test_disconnect_unsuccessful_flow(mocker, connection, caplog):
    # Initialisation
    mocker.patch.object(connection, "_perform_disconnection")
    connection._connected = True
    connection._ib.isConnected.return_value = True
    # Start the test
    with caplog.at_level("ERROR"), pytest.raises(TWSConnectionError):
        connection.disconnect()
    # Assertions for test validation
    assert connection._connected is True
    assert any(record.levelname == "ERROR" for record in caplog.records)

def test_disconnect_with_active_connection(connection, caplog):
    # Initialisation
    connection._connected = False
    # Start the test
    with caplog.at_level("ERROR"), pytest.raises(TWSConnectionError):
        connection.disconnect()
    # Assertions for test validation
    assert connection._connected is False
    assert any(record.levelname == "ERROR" for record in caplog.records)