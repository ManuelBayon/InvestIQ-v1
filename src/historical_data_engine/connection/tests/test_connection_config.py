from historical_data_engine.connection.ConnectionConfig import ConnectionConfig
from backtest_engine.Enums import TradingMode

def test_paper_config():
    config = ConnectionConfig.paper()
    assert config._host == "127.0.0.1"
    assert config._port == 7497
    assert config._client_id == 1
    assert config._mode == TradingMode.PAPER