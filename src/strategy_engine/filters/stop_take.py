import pandas as pd

from strategy_engine.filters.base_filter import BaseFilter


class StopTakeFilter(BaseFilter):

    def __init__(
        self,
        sl_pct: float = 0.01,
        tp_pct: float = 0.02,
        cooldown: int = 10
    ):
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.cooldown = cooldown

    def apply_filter(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df["target_position"] = 0
        df["entry_price"] = None
        df["cooldown_remaining"] = 0

        current_position = 0
        entry_price = None
        cooldown_rem = 0

        for i in range(len(df)):
            price = df.at[i, "close"]
            raw = df.at[i, "raw_target"]

            # Cooldown actif
            if cooldown_rem > 0:
                cooldown_rem -= 1
                current_position = 0

            else:
                # Pas en position => entrée possible
                if current_position == 0:
                    if raw != 0:
                        current_position = raw
                        entry_price = price

                # En position => vérifier SL/TP
                else:
                    pnl_pct = (price - entry_price) / entry_price
                    dir_pnl = pnl_pct if current_position > 0 else -pnl_pct

                    if dir_pnl >= self.tp_pct:
                        current_position = 0
                        cooldown_rem = self.cooldown

                    elif dir_pnl <= -self.sl_pct:
                        current_position = 0
                        cooldown_rem = self.cooldown

            df.at[i, "target_position"] = current_position
            df.at[i, "entry_price"] = entry_price
            df.at[i, "cooldown_remaining"] = cooldown_rem

        return df