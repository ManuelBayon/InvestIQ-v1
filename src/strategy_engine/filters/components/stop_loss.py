import datetime
import uuid

from strategy_engine.filters.abstract_filter import AbstractFilter, FilterMetadata
from strategy_engine.strategies.contracts import FilterInput, FilterOutput, MarketField


class StaticStopLossFilter(AbstractFilter):

    def __init__(
        self,
        sl_pct: float = 0.01,
        cooldown: int = 10
    ):
        self.sl_pct = sl_pct
        self.cooldown = cooldown
        self.metadata = FilterMetadata(
            filter_uuid=str(uuid.uuid4()),
            created_at=datetime.datetime.now().isoformat(),
            name="StaticStopLossFilter",
            version="1.0.0",
            description="Applies a static stop-loss based on a fixed percentage "
                        "drop from the entry price. Does not trail. "
                        "Each position receives a fixed stop price at entry.",
            parameters={
                "sl_pct": self.sl_pct,
                "cooldown": self.cooldown,
            },
            required_fields=[
                MarketField.CLOSE
            ],
            produced_features=[
                "stop_price",
                "sl_triggered",
                "latent_pnl",
            ],
            diagnostics_schema=[
                "stop_price",
                "sl_triggered",
                "latent_pnl",
            ]
        )

    def apply_filter(
            self,
            input_: FilterInput
    ) -> FilterOutput:

        for field in self.metadata.required_fields:
            if field not in input_.features:
                raise KeyError(f"Missing required field {field}")

        ts  = input_.timestamp
        close = input_.features[MarketField.CLOSE]

        # Compléter la stratégie de stop loss ici
        # ...

        return FilterOutput(
            timestamp=input_.timestamp,
            target_position= ,
            diagnostics=,
        )