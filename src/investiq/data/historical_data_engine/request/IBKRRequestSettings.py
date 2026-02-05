from dataclasses import dataclass

from ib_insync import Contract

from investiq.data.historical_data_engine.enums import BarSize, WhatToShow
from investiq.data.historical_data_engine.instruments.AbstractInstrumentSettings import InstrumentSettings
from investiq.data.historical_data_engine.request.AbstractRequestSettings import RequestSettings


@dataclass
class IBKRRequestSettings(RequestSettings):
    duration : str
    bar_size_setting: BarSize = BarSize.ONE_DAY
    end_date_time: str = ""
    use_RTH: bool = False
    what_to_show: WhatToShow = WhatToShow.MIDPOINT
    def with_defaults_from(
            self,
            instrument : InstrumentSettings
    ) -> "IBKRRequestSettings":
        return IBKRRequestSettings(
            duration=self.duration,
            what_to_show=self.what_to_show or instrument.default_what_to_show(),
            bar_size_setting=self.bar_size_setting,
            end_date_time=self.end_date_time,
            use_RTH=self.use_RTH
        )
    def to_query_kwargs(self, contract : Contract) -> dict:
        return {
            "contract": contract,
            "endDateTime": self.end_date_time,
            "durationStr": self.duration,
            "barSizeSetting": self.bar_size_setting.value,
            "whatToShow": self.what_to_show.value,
            "useRTH": self.use_RTH,
        }