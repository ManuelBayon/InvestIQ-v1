from collections.abc import Iterator

import pandas as pd

from investiq.api.market import MarketEvent, OHLCV
from investiq.data.historical_data_engine.enums import BarSize
from investiq.utilities.logger.protocol import LoggerProtocol

class DataFrameBacktestFeed:

    def __init__(
            self,
            logger: LoggerProtocol,
            df: pd.DataFrame,
            symbol: str,
            bar_size: BarSize) -> None:
        self._logger = logger
        self._df = df
        self._symbol = symbol
        self._bar_size = bar_size

    def __iter__(self) -> Iterator[MarketEvent]:
        df = self._df

        if "timestamp" in df.columns:
            ts_iter = df["timestamp"]
            rows = df.drop(columns=["timestamp"])
        else:
            ts_iter = df.index
            rows = df

        prev_ts = None
        n = len(df)
        self._logger.info(f"FEED events={n}")
        if n == 0:
            return

        for ts, row in zip(ts_iter, rows.itertuples(index=False)):
            # 1) monotonic
            if prev_ts is not None and ts < prev_ts:
                raise ValueError(f"Non-monotonic timestamps: {ts} < {prev_ts}")
            prev_ts = ts

            o = float(getattr(row, "open"))
            h = float(getattr(row, "high"))
            l = float(getattr(row, "low"))
            c = float(getattr(row, "close"))
            v_raw = getattr(row, "volume", 0.0)
            v = 0.0 if v_raw is None else float(v_raw)

            # 2) OHLC invariant
            if not (l <= min(o, c) and max(o, c) <= h):
                raise ValueError(f"Invalid OHLC at {ts}: o={o} h={h} l={l} c={c}")

            yield MarketEvent(
                timestamp=ts,
                bar=OHLCV(open=o, high=h, low=l, close=c, volume=v),
                symbol=self._symbol,
                bar_size=self._bar_size,
            )
