from abc import ABC, abstractmethod

from ib_insync import Contract

from investiq.data.legagy_data_engine.enums import BarSize, WhatToShow


class RequestSettings(ABC):
    duration : str
    bar_size_setting : BarSize = BarSize.ONE_DAY
    what_to_show : WhatToShow
    @abstractmethod
    def to_query_kwargs(self, contract : Contract) -> dict:
        pass