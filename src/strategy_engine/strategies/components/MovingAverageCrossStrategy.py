import datetime
import uuid

import pandas as pd

from strategy_engine.strategies.abstract_strategy import AbstractStrategy, StrategyMetadata
from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, MarketField


class MovingAverageCrossStrategy(AbstractStrategy):

    def __init__(
            self,
            fast_window: int = 20,
            slow_window:int = 100
    ):
        self.fast_window= fast_window
        self.slow_window= slow_window
        self.metadata = StrategyMetadata(
            strategy_uuid=str(uuid.uuid4()),
            created_at=datetime.datetime.now().isoformat(),
            name="MovingAverageCrossStrategy",
            version="1.0.0",
            description="Simple moving-average crossover strategy.",
            parameters= {
                "fast_window": fast_window,
                "slow_window": slow_window
            },
            required_fields=[MarketField.CLOSE],
            produced_features=["ma_fast", "ma_slow"],
            price_type=MarketField.CLOSE,
        )

    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:

        for field in self.metadata.required_fields:
            if field not in input_.data:
                raise KeyError(f"Missing required field: {field}")

        ts = input_.timestamp
        close = input_.data[MarketField.CLOSE]

        ma_fast= close.rolling(window=self.fast_window).mean()
        ma_slow = close.rolling(window=self.slow_window).mean()

        raw_target = (ma_fast > ma_slow).astype(int) - (ma_fast < ma_slow).astype(int)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            price_type=MarketField.CLOSE,
            price_serie=close,
            metadata=self.metadata,
            features={
                "ma_fast": ma_fast,
                "ma_slow": ma_slow,
            },
            diagnostics={}
        )