import pandas as pd

from strategy_engine.filters.base_filter import BaseFilter


class StaticStopLossFilter(BaseFilter):

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

        # --- Coder Stop Loss Ici --- #


        return df