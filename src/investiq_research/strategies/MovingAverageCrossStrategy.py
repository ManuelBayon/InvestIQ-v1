from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.market import MarketField
from investiq.api.strategy import StrategyMetadata


class MovingAverageCrossStrategy:

    def __init__(
            self,
            fast_window: int = 20,
            slow_window: int = 100
    ):
        if fast_window <= 0 or slow_window <= 0:
            raise ValueError("fast_window and slow_window must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be < slow_window for a classic MA cross")

        self.metadata = StrategyMetadata(
            name="MovingAverageCross",
            version="1.0.0",
            description="Simple moving-average crossover strategy (event-driven).",

            parameters={
                "fast_window": fast_window,
                "slow_window": slow_window,
            },

            price_type=MarketField.CLOSE,
            required_fields=frozenset({MarketField.CLOSE}),
            produced_features=frozenset({"ma_fast", "ma_slow"}),
        )

    def decide(self, view: BacktestView) -> Decision:
       ...