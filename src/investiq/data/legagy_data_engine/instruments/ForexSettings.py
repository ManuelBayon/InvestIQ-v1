from dataclasses import dataclass

from ib_insync import Forex

from engine.historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from engine.historical_data_engine.enums import Exchange, AssetType, WhatToShow
from engine.historical_data_engine.instruments.InstrumentID import InstrumentID


@dataclass
class ForexSettings(InstrumentSettings):
    pair : str
    symbol_id: InstrumentID
    exchange : Exchange = Exchange.IDEALPRO
    asset_type : AssetType = AssetType.FOREX

    def to_contract(self):
        return Forex(
            pair=self.pair,
            exchange=self.exchange.value,
        )
    def default_what_to_show(self) -> str:
        return WhatToShow.MIDPOINT.value

    def get_display_name(self) -> str:
        return self.pair