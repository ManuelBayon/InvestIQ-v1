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

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:

        df = data.copy()

        # Étape 1 : Signal brut
        df = self.generate_raw_signal(df)

        # Étape 2 : filtre SL / TP / cooldown
        return self.apply_stop_filter(df)

    def generate_raw_signal(self, data: pd.DataFrame) -> pd.DataFrame:
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

    def apply_stop_filter(
            self,
            data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Étape 2 : applique SL / TP / cooldown sur le signal brut.
        - sl_pct    : stop loss en pourcentage
        - tp_pct    : take profit en pourcentage
        - cooldown  : nombre de bougies où les positions sont interdites après un stop
        """

        df = data.copy()
        df["target_position"] = 0
        df["entry_price"] = None
        df["cooldown_remaining"] = 0

        current_position = 0
        entry_price = None
        cooldown_remaining = 0

        for i in range (len(df)):

            price = df.at[i, "close"]
            raw = df.at[i, "raw_target"]

            # Cooldown actif => interdiction de position
            if cooldown_remaining != 0:
                current_position = 0
                cooldown_remaining -= 1


            else:
                # si pas en position => possibilité d'entrer
                if current_position == 0:
                    if raw != 0: # entrée sur raw signal
                        current_position = raw
                        entry_price = price
                else:
                    raw_return = (price - entry_price) / entry_price
                    dir_return = raw_return if current_position > 0 else -raw_return

                    # Take Profit
                    if dir_return >= self.tp_pct:
                        current_position = 0
                        cooldown_remaining = self.cooldown

                    # Stop Loss
                    elif dir_return <= -self.sl_pct:
                        current_position = 0
                        cooldown_remaining = self.cooldown


                    # Sinon, on maintient la position

            df.at[i, "target_position"] = current_position
            df.at[i, "entry_price"] = entry_price
            df.at[i, "cooldown_remaining"] = cooldown_remaining

        # Harmonisation du timestamp
        df["timestamp"] = df["date"]
        return df[["timestamp", "close", "target_position"]]