import datetime
import uuid
from collections.abc import Sequence

from backtest_engine.common.contracts import BacktestContext
from strategy_engine.strategies.abstract_strategy import AbstractStrategy, StrategyMetadata
from strategy_engine.contracts import StrategyInput, StrategyOutput, MarketField


class MovingAverageCrossStrategy(AbstractStrategy):

    def __init__(
            self,
            fast_window: int = 20,
            slow_window: int = 100
    ):
        self.fast_window= fast_window
        self.slow_window= slow_window
        self.metadata = StrategyMetadata(
            strategy_uuid=str(uuid.uuid4()),
            created_at=datetime.datetime.now().isoformat(),
            name="MovingAverageCrossStrategy",
            version="1.0.0",
            description="Simple moving-average crossover strategy (event-driven).",
            parameters= {
                "fast_window": fast_window,
                "slow_window": slow_window
            },
            required_fields=[MarketField.CLOSE],
            produced_features=["ma_fast", "ma_slow"],
            price_type=MarketField.CLOSE,
        )
    @staticmethod
    def _compute_sma_incremental(
            window_size: int,
            previous_sma: float | None,
            hist_close: Sequence[float],
    ) -> float | None:

        len_hist_close = len(hist_close)

        # Not enough data
        if len_hist_close < window_size:
            return None

        # First full window : compute full SMA
        if len_hist_close == window_size:
            return sum(hist_close[-window_size:]) / window_size

        # Incremental update
        close_t = hist_close[-1]
        close_out = hist_close[-window_size - 1]
        return previous_sma + (close_out - close_t)/window_size

    def generate_raw_signals(
            self,
            strategy_input: StrategyInput,
            context: BacktestContext | None = None
    ) -> StrategyOutput:

        for field in self.metadata.required_fields:
            if field not in strategy_input.bar:
                raise KeyError(f"Missing required field: {field}")

        ts = strategy_input.timestamp
        close = strategy_input.bar[MarketField.CLOSE]
        hist_close = strategy_input.history[MarketField.CLOSE]


        # 1. Compute features incrementally
        prev_fast = context.features.get("ma_fast")
        prev_slow = context.features.get("ma_slow")

        ma_fast = self._compute_sma_incremental(
            window_size=self.fast_window,
            previous_sma=prev_fast,
            hist_close=hist_close,
        )
        ma_slow = self._compute_sma_incremental(
            window_size=self.slow_window,
            previous_sma=prev_slow,
            hist_close=hist_close,
        )

        # 2. Update context features
        context.features["ma_fast"] = ma_fast
        context.features["ma_slow"] = ma_slow

        context.features_history.setdefault("ma_fast", []).append(ma_fast)
        context.features_history.setdefault("ma_slow", []).append(ma_slow)

        #2. Warmup logic
        if ma_fast is None or ma_slow is None:
            return StrategyOutput(
                timestamp=ts,
                raw_target=0,
                price=close,
                price_type=MarketField.CLOSE,
                metadata=self.metadata,
                diagnostics={"warming_up": True},
            )

        # 3. Trading logic
        raw_target = int(ma_fast > ma_slow) - int(ma_fast < ma_slow)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            price=close,
            price_type=MarketField.CLOSE,
            metadata=self.metadata,
            diagnostics={},
        )