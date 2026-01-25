from dataclasses import dataclass

from invest_iq.engines.historical_data_engine.enums import TradingMode


@dataclass
class ConnectionConfig:
    host : str
    port : int
    client_id : int
    _mode : TradingMode

    @classmethod
    def paper(cls) -> "ConnectionConfig":
        return cls(host="127.0.0.1", port=7497, client_id=1, _mode=TradingMode.PAPER)

    @classmethod
    def live(cls) -> "ConnectionConfig":
        return cls(host="127.0.0.1", port=7496, client_id=2, _mode=TradingMode.LIVE)

    @property
    def mode(self) -> TradingMode:
        return self._mode