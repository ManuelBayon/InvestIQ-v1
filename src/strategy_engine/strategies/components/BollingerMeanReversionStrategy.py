import datetime
import uuid

from strategy_engine.strategies.abstract_strategy import AbstractStrategy, StrategyMetadata

from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, MarketField, ComponentType


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
        self.metadata = StrategyMetadata(
            strategy_uuid=str(uuid.uuid4()),
            created_at=datetime.datetime.now().isoformat(),
            name="BollingerMeanReversion",
            version="1.0.0",
            description="Mean reversion strategy using Bollinger bands.",
            parameters={
                "window": window,
                "num_std": num_std,
                "sl_pct": sl_pct,
                "tp_pct": tp_pct,
                "cooldown": cooldown
            },
            required_fields=[MarketField.CLOSE],
            produced_features=["std", "middle", "upper", "lower"],
            price_type=MarketField.CLOSE
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

        std = close.rolling(self.window).std()
        middle = close.rolling(self.window).mean()
        upper = middle + self.num_std * std
        lower = middle - self.num_std * std

        raw_target = (close < lower).astype(int) - (close > upper).astype(int)

        return StrategyOutput(
            timestamp=ts,
            raw_target=raw_target,
            price_type=MarketField.CLOSE,
            price_serie=close,
            metadata=self.metadata,
            features={
                "std": std,
                "middle": middle,
                "upper": upper,
                "lower": lower,
            },
            diagnostics = {},
        )