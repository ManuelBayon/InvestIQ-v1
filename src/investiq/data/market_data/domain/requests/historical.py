from dataclasses import dataclass

from investiq.data.market_data.domain.enums import BarSize, WhatToShow
from investiq.data.market_data.domain.requests.base import RequestSpec


@dataclass(frozen=True)
class HistoricalRequestSpec(RequestSpec):
    duration: str
    bar_size: BarSize = BarSize.ONE_DAY
    what_to_show: WhatToShow = WhatToShow.MIDPOINT