from collections.abc import Iterator

from invest_iq.common.market_types import MarketEvent, OHLCV
from invest_iq.engines.backtest_engine.common.contracts import BacktestInput
from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


class BacktestFeed:

    def __init__(
            self,
            logger: LoggerProtocol,
            bt_input: BacktestInput
    ) -> None:
        self._logger = logger
        self.events = bt_input.events

    def __iter__(self) -> Iterator[MarketEvent]:

        events = self.events
        n = len(events)

        self._logger.info(f"FEED events={n}")
        if n == 0:
            self._logger.info("FEED empty")
            return

        e0 = events[0]
        self._logger.info(f"FEED first ts={e0.timestamp}, close ={e0.bar.close}")

        prev_timestamp = None

        for e in events:
            # 1) Monotonic timestamp
            if prev_timestamp is not None and e.timestamp < prev_timestamp:
                raise ValueError(f"Non-monotonic timestamps: {e.timestamp} < {prev_timestamp}")
            prev_timestamp = e.timestamp

            # 2) Volume normalisation
            bar = e.bar
            vol = 0.0 if bar.volume is None else float(bar.volume)

            # 3) OHLC value check
            if not (
                    bar.low <= min(bar.open, bar.close) and
                    max(bar.open, bar.close) <= bar.high
            ):
                raise ValueError(f"Invalid OHLC at {e.timestamp}: {bar}")

            # yield event (only if volume has been modified)
            if bar.volume is None or bar.volume != vol:
                yield MarketEvent(
                    timestamp=e.timestamp,
                    bar=OHLCV(
                        open=bar.open,
                        high=bar.high,
                        low=bar.low,
                        close=bar.close,
                        volume=vol,
                    ),
                    symbol=e.symbol,
                    bar_size=e.bar_size,
                )
            else:
                yield e