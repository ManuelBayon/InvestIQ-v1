import pandas as pd

from strategy_engine.AbstractStrategy import AbstractStrategy

class MovingAverageCrossStrategy(AbstractStrategy):

    def __init__(self, fast_window: int, slow_window:int):
        self.fast_window= fast_window
        self.slow_window= slow_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        df['ma_fast']=df['close'].rolling(window=self.fast_window).mean()
        df['ma_slow'] = df['close'].rolling(window=self.slow_window).mean()

        df["target_position"] = 0
        df.loc[df["ma_fast"] > df["ma_slow"], "target_position"] = 1
        df.loc[df["ma_fast"] < df["ma_slow"], "target_position"] = -1

        df["target_position"] = df["target_position"].fillna(0)
        df["timestamp"]= df["date"]

        return df[["timestamp", "close", "ma_fast", "ma_slow", "target_position"]]