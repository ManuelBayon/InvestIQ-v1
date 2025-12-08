import pandas as pd

from strategy_engine.filters.abstract_filter import AbstractFilter, FilterMetadata
from strategy_engine.strategies.contracts import FilterInput, FilterOutput, MarketField


class StaticStopLossFilter(AbstractFilter):

    metadata = FilterMetadata(
        name='StaticStopLoss',
        version="1.0",
        description="Statical Stop loss in %",
    )

    def __init__(
        self,
        sl_pct: float = 0.01,
        tp_pct: float = 0.02,
        cooldown: int = 10
    ):
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.cooldown = cooldown

    def apply_filter(
            self,
            input_: FilterInput
    ) -> FilterOutput:

        raw_target = input_.raw_target
        price_series = input_.price_serie

        # Code here Stop-loss filter
        # ...

        return FilterOutput(
            timestamp = input_.timestamp,
            target_position = pd.Series(),
            price_type = input_.price_type,
            price_serie = input_.price_serie,
        )