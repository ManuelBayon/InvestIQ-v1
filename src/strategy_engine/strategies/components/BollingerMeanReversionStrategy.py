from strategy_engine.strategies.abstract_strategy import AbstractStrategy, StrategyMetadata
import pandas as pd

from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, MarketField


class BollingerMeanReversionStrategy(AbstractStrategy):

    metadata = StrategyMetadata(
        name="BollingerMeanReversion",
        version="v1",
        description="Mean reversion strategy using Bollinger bands."
    )

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

    @property
    def name(self) -> str:
        return "BollingerMeanReversion"

    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:

        ts = input_.timestamp
        close = input_.data[MarketField.CLOSE]

        std = close.rolling(self.window).std()
        middle = close.rolling(self.window).mean()
        upper = middle + self.num_std * std
        lower = middle - self.num_std * std

        raw_target = (close < lower).astype(int) - (close > upper).astype(int)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            signal_price=MarketField.CLOSE,
            signal_price_series=close,
            diagnostics = {
                "std": pd.Series(std),
                "middle": pd.Series(middle),
                "upper": pd.Series(upper),
                "lower": pd.Series(lower),
            },
        )