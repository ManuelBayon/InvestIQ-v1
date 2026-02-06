from collections.abc import Iterator
from typing import Final

import pandas as pd

from investiq.api.market import MarketEvent, OHLCV
from investiq.data.legagy_data_engine.enums import BarSize
from investiq.data.market_data.normalize import normalize_timestamp_column, standardize_timestamp_utc, validate_ohlc

_CANONICAL_TS: Final[str] = "timestamp"

class DataFrameBacktestFeed:
    """
    Canonical feed for the backtest pipeline.

    Input: a pandas DataFrame from ANY datasource (IBKR, CSV, Parquet, etc.)
    Output: an iterator of MarketEvent with canonical OHLCV bars.

    Guarantees after __init__:
    - timestamp column exists and is canonical (_CANONICAL_TS)
    - timestamps are UTC-naive (canonical)
    - OHLCV invariants validated once
    """
    def __init__(
            self,
            df: pd.DataFrame,
            symbol: str,
            bar_size: BarSize,
            enforce_utc: bool = True,
    ):
        df = normalize_timestamp_column(
            df=df,
            canonical=_CANONICAL_TS,
        )
        if enforce_utc:
            df = standardize_timestamp_utc(df=df)
        validate_ohlc(df=df)
        self._df = df
        self._symbol = symbol
        self._bar_size = bar_size

    def __iter__(self) -> Iterator[MarketEvent]:
        df = self._df

        # This assumes timestamp column exists (guaranteed by __init__)
        ts_iter = df[_CANONICAL_TS]
        rows = df.drop(columns=[_CANONICAL_TS]).itertuples(index=False)

        for ts, row in zip(ts_iter, rows):
            # minimal conversion cost (per-row)
            o = float(getattr(row, "open"))
            h = float(getattr(row, "high"))
            l = float(getattr(row, "low"))
            c = float(getattr(row, "close"))
            v_raw = getattr(row, "volume")
            v = 0.0 if v_raw is None else float(v_raw)

            yield MarketEvent(
                timestamp=ts,
                bar=OHLCV(open=o, high=h, low=l, close=c, volume=v),
                symbol=self._symbol,
                bar_size=self._bar_size,
            )