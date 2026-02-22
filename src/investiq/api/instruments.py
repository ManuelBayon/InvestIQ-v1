from dataclasses import dataclass
from enum import StrEnum

from investiq.market_data import BarSize


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