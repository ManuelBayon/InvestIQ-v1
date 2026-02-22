from abc import ABC
from dataclasses import dataclass

from investiq.market_data.domain.enums import BarSize, WhatToShow


@dataclass(frozen=True)
class RequestSpec(ABC):
    duration: str
    bar_size: BarSize = BarSize.ONE_DAY
    what_to_show: WhatToShow = WhatToShow.MIDPOINT