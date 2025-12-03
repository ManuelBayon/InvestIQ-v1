from dataclasses import dataclass

from ib_insync import Stock

from historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from backtest_engine.Enums import Exchange, Currency, AssetType, WhatToShow
from historical_data_engine.instruments.InstrumentID import InstrumentID


@dataclass
class StockSettings(InstrumentSettings):
    symbol : str
    symbol_id: InstrumentID
    exchange : Exchange = Exchange.NYSE
    currency : Currency = Currency.USD
    asset_type : AssetType = AssetType.STOCK

    def to_contract(self):
        return Stock(
            symbol=self.symbol,
            exchange=self.exchange.value,
            currency=self.currency.value
        )
    def default_what_to_show(self) -> str:
        return WhatToShow.MIDPOINT.value

    def get_display_name(self) -> str:
        return self.symbol