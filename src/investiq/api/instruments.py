from dataclasses import dataclass
from enum import StrEnum

from investiq.data.historical_data_engine.enums import BarSize


class AssetClass(StrEnum):
    CONT_FUT = "CONT_FUT"

@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    asset_class: AssetClass
    bar_size: BarSize
    timezone: str | None = None

class FutureCME(StrEnum):
    MNQ = "MNQ"