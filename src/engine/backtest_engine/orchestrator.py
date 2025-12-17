from collections.abc import Iterator
from dataclasses import dataclass

import pandas as pd

from engine.backtest_engine.common.contracts import BacktestContext, BacktestInput
from engine.backtest_engine.engine import BacktestEngine


@dataclass(frozen=True)
class CandleSnapshot:
    timestamp: pd.Timestamp
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

class BacktestOrchestrator:

    def __init__(
            self,
            engine: BacktestEngine,
            context: BacktestContext,
    ):
        self._engine = engine
        self._context = context

    def stream_candles(
            self,
            bt_input: BacktestInput
    ) -> Iterator[CandleSnapshot]:

        n = len(bt_input.timestamp)

        for i in range(n):

            self._engine.step(
                bt_input=bt_input,
                context=self._context,
                i=i
            )

            bar = self._context.bar

            snapshot = CandleSnapshot(
                timestamp=self._context.timestamp,
                open=bar["open"],
                high=bar["high"],
                low=bar["low"],
                close=bar["close"]
            )
            yield snapshot