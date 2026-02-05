from types import MappingProxyType

from investiq.api.market import MarketEvent, MarketField, MarketView
from investiq.core.errors import ContextNotInitializedError


class MarketStore:

    def __init__(self):
        self._snapshot: MarketEvent | None = None
        self._history: dict[MarketField, list[float]] = {}

    def ingest(self, event: MarketEvent) -> None:
        self._snapshot = event
        for k, v in event.bar.items():
            self._history.setdefault(MarketField(k), []).append(v)

    def view(self) -> MarketView:
        if self._snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        # freeze lists into tuples (no accidental mutation)
        frozen = {k: tuple(v) for k, v in self._history.items()}
        return MarketView(
            snapshot=self._snapshot,
            history=MappingProxyType(frozen),
        )