import pandas as pd

from strategy_engine.strategies.abstract_strategy import AbstractStrategy
from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, SignalPrice


class MovingAverageCrossStrategy(AbstractStrategy):

    def __init__(
            self,
            fast_window: int = 20,
            slow_window:int = 100
    ):
        self.fast_window= fast_window
        self.slow_window= slow_window

    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:

        ts = input_.timestamp
        close = input_.close

        ma_fast= close.rolling(window=self.fast_window).mean()
        ma_slow = close.rolling(window=self.slow_window).mean()

        raw_target = (ma_fast > ma_slow) - (ma_fast < ma_slow)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            signal_price=SignalPrice.CLOSE,
            signal_price_series=close,
            diagnostics=pd.DataFrame({
                "ma_fast": ma_fast,
                "ma_slow": ma_slow,
            })
        )