from dataclasses import dataclass

from ib_insync import ContFuture, Contract

from investiq.data.legagy_data_engine.enums import Exchange, Currency, AssetType, WhatToShow
from investiq.data.legagy_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from investiq.data.legagy_data_engine.instruments.InstrumentID import InstrumentID


@dataclass
class ContFutureSettings(InstrumentSettings):
    symbol: str
    symbol_id: InstrumentID
    exchange: Exchange = Exchange.CME
    currency: Currency = Currency.USD
    asset_type: AssetType = AssetType.CONT_FUTURE

    def to_contract(self) -> Contract:
        return ContFuture(
            symbol=self.symbol,
            exchange=self.exchange.value,
            currency=self.currency.value
        )
    def default_what_to_show(self) -> WhatToShow:
        return WhatToShow.MIDPOINT

    def get_display_name(self) -> str:
        return self.symbol
