from strategy_engine.strategies.abstract_strategy import AbstractStrategy
import pandas as pd

from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, SignalPrice


class BollingerMeanReversionStrategy(AbstractStrategy):

    def __init__(
        self,
        window: int = 20,
        num_std: float = 2.0,
        sl_pct: float = 0.01,
        tp_pct: float = 0.02,
        cooldown: int = 10
    ):
        self.window = window
        self.num_std = num_std
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.cooldown = cooldown

    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:

        ts = input_.timestamp
        close = input_.close

        std = close.rolling(self.window).std()
        middle = close.rolling(self.window).mean()
        upper = middle + self.num_std * std
        lower = middle - self.num_std * std

        raw_target = (close < lower).astype(int) - (close > upper).astype(int)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            signal_price=SignalPrice.CLOSE,
            signal_price_series=close,
            diagnostics=pd.DataFrame({
                "std": std,
                "middle": middle,
                "upper": upper,
                "lower": lower,
            }),
        )