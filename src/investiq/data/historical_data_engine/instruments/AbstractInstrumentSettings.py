from abc import ABC, abstractmethod
from typing import Optional, Protocol

from investiq.data.historical_data_engine.enums import AssetType, Exchange
from investiq.data.historical_data_engine.instruments.InstrumentID import InstrumentID

class BrokerContract(Protocol):
    """Generic interface for a broker contract (IBKR, Binance, FIX...)."""
    ...

class InstrumentSettings(ABC):
    asset_type: AssetType
    symbol_id: InstrumentID
    symbol: str
    currency: str
    exchange: Optional[Exchange] = None
    local_symbol: Optional[str] = None

    @abstractmethod
    def to_contract(self) -> BrokerContract:
        ...

    @abstractmethod
    def default_what_to_show(self) -> str:
        ...

    @abstractmethod
    def get_display_name(self) -> str:
        ...