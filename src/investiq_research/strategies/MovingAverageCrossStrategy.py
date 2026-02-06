from collections.abc import Sequence

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

        if fast_window <= 0 or slow_window <= 0:
            raise ValueError("fast_window and slow_window must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be < slow_window for a classic MA cross")

        self.fast_window= fast_window
        self.slow_window= slow_window

        self._ma_fast: float | None = None
        self._ma_slow: float | None = None

    def reset(self) -> None:
        """
        Call this at the start of each run if you reuse the instance.
        """
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
        close = bar.close

        history = view.market.history.get(MarketField.CLOSE)
        if history is None:
            raise KeyError("No close history available")

        n = len(history)

        #1 Update indicators if enough history
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

        # 2. Return canonical Decision (target_position == 0)
        if self._ma_fast is None or self._ma_slow is None:
            return Decision(
                timestamp=ts,
                target_position=0.0,
                execution_price=close,
                diagnostics={
                    "warming_up": True,
                    "n": n,
                    "fast_window": self.fast_window,
                    "slow_window": self.slow_window,
                },
            )

        # 3. Trading logic
        if self._ma_fast > self._ma_slow:
            raw_target = 1
        elif self._ma_fast < self._ma_slow:
            raw_target = -1
        else:
            raw_target = 0

        # 4. Return Decision
        return Decision(
            timestamp=ts,
            target_position=float(raw_target),
            execution_price=close,
            diagnostics={
                "ma_fast": self._ma_fast,
                "ma_slow": self._ma_slow,
            },
        )