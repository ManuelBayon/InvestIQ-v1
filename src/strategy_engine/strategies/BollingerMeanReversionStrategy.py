from strategy_engine.AbstractStrategy import AbstractStrategy
import pandas as pd


class BollingerMeanReversionStrategy(AbstractStrategy):

    def __init__(
        self,
        window: int = 20,
        num_std: float = 2.0,
        sl_pct: float = 0.01,
        tp_pct: float = 0.02,
        cooldown: int = 10
    ):
        """
        Stratégie de retour à la moyenne basée sur les bandes de Bollinger.
        """
        self.window = window
        self.num_std = num_std
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.cooldown = cooldown

    def generate_raw_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Produit le signal brut (non filtré).
        """
        df = data.copy()

        # Bande centrale : moyenne mobile
        df["middle"] = df["close"].rolling(self.window).mean()

        # Écart-type
        df["std"] = df["close"].rolling(self.window).std()

        # Bandes de Bollinger
        df["upper"] = df["middle"] + self.num_std * df["std"]
        df["lower"] = df["middle"] - self.num_std * df["std"]

        # Initialisation de la position cible
        df["raw_target"] = 0

        # Règles :
        df.loc[df["close"] < df["lower"], "raw_target"] = +1 # Acheter
        df.loc[df["close"] > df["upper"], "raw_target"] = -1 # Vendre

        return df