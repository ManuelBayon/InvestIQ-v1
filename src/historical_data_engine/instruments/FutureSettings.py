from dataclasses import dataclass

from ib_insync import Future

from historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from historical_data_engine.enums import Exchange, Currency, AssetType, WhatToShow
from historical_data_engine.instruments.InstrumentID import InstrumentID


@dataclass
class FutureSettings(InstrumentSettings):
    symbol: str
    local_symbol: str
    symbol_id: InstrumentID
    exchange : Exchange = Exchange.CME
    currency : Currency = Currency.USD
    asset_type : AssetType = AssetType.FUTURE

    def to_contract(self):
        return Future(
            symbol=self.symbol,
            localSymbol=self.local_symbol,
            exchange=self.exchange.value,
            currency=self.currency.value,
        )
    def default_what_to_show(self) -> str:
        return WhatToShow.MIDPOINT.value

    def get_display_name(self) -> str:
        return self.symbol
