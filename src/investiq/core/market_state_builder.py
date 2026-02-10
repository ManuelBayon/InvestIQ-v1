from types import MappingProxyType

from investiq.api.market import MarketDataEvent, MarketField, MarketSate
from investiq.core.errors import ContextNotInitializedError


class MarketStateBuilder:
    """
    Ingests MarketDataEvent streams and maintains the current canonical market state.

    Updates rolling per-field history at each event and exposes an immutable
    MarketState snapshot via `view()`, ensuring downstream components read a
    consistent, read-only representation of the latest market data.
    """
    def __init__(self):
        self._snapshot: MarketDataEvent | None = None
        self._history: dict[MarketField, list[float]] = {}

    def ingest(self, event: MarketDataEvent) -> None:
        self._snapshot = event
        for k, v in event.bar.items():
            self._history.setdefault(MarketField(k), []).append(v)

    def view(self) -> MarketSate:
        if self._snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        # freeze lists into tuples (no accidental mutation)
        frozen = {k: tuple(v) for k, v in self._history.items()}
        return MarketSate(
            snapshot=self._snapshot,
            history=MappingProxyType(frozen),
        )