import datetime
import uuid
from collections.abc import Sequence

from invest_iq.engines.backtest_engine.common.types import BacktestView, Decision, MarketField
from invest_iq.engines.strategy_engine.strategies.abstract_strategy import AbstractStrategy, StrategyMetadata

class MovingAverageCrossStrategy(AbstractStrategy):

    def __init__(
            self,
            fast_window: int = 20,
            slow_window: int = 100
    ):
        if fast_window <= 0 or slow_window <= 0:
            raise ValueError("fast_window and slow_window must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be < slow_window for a classic MA cross")

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

        self._ma_fast: float | None = None
        self._ma_slow: float | None = None

    def reset(self) -> None:
        """Call this at the start of each run if you reuse the instance."""
        self._ma_fast = None
        self._ma_slow = None

    @staticmethod
    def _compute_sma_incremental(
            window_size: int,
            previous_sma: float | None,
            history: Sequence[float],
    ) -> float | None:

        n = len(history)
        if n < window_size:
            return None
        if n == window_size:
            return sum(history[-window_size:]) / window_size

        close_t = history[-1]
        close_out = history[-window_size - 1]
        return previous_sma + (close_t - close_out) / window_size

    def decide(self, view: BacktestView) -> Decision:
        ts = view.market.timestamp
        bar = view.market.bar

        history = view.market.history.get(MarketField.CLOSE)
        if history is None:
            raise KeyError("No close history available")

        close = bar.close
        n = len(history)

        if n >= self.fast_window:
            self._ma_fast = self._compute_sma_incremental(
                window_size=self.fast_window,
                previous_sma=self._ma_fast,
                history=history,
            )
        if n >= self.slow_window:
            self._ma_slow = self._compute_sma_incremental(
                window_size=self.slow_window,
                previous_sma=self._ma_slow,
                history=history,
            )

        #2. Warmup logic
        if (
            n < self.slow_window
            or self._ma_fast is None
            or self._ma_slow is None
        ):
            return Decision(
                timestamp=ts,
                target_position=0.0,
                execution_price=close,
                diagnostics={
                    "warming_up": True,
                    "n":n
                },
            )

        # 3. Trading logic
        raw_target = int(self._ma_fast > self._ma_slow) - int(self._ma_fast < self._ma_slow)

        return Decision(
            timestamp=ts,
            target_position=float(raw_target),
            execution_price=close,
            diagnostics={
                "ma_fast": self._ma_fast,
                "ma_slow": self._ma_slow,
            },
        )