from dataclasses import dataclass, field

import pandas as pd

from invest_iq.common.market_types import OHLCV, MarketEvent
from invest_iq.engines.backtest_engine.common.contracts import ModelState, ExecutionState


class ContextNotInitializedError(Exception):
    pass

@dataclass
class BacktestContext:
    """
    Runtime state of a backtest/live session.

    This object represents the *current system state* at a given market event.
    It is mutated step-by-step by the Engine.

    Design principles:
    - `snapshot` holds the current market event (timestamp + bar)
    - `history` holds accumulated past values (for indicators/strategies)
    - `model` holds the last strategy/filter/orchestrator outputs
    - `execution` holds the portfolio/execution state
    """

    # Model / execution state
    model : ModelState = field(default_factory=ModelState)
    execution : ExecutionState = field(default_factory=ExecutionState)

    # Current market snapshot (None before the first event is processed)
    snapshot: MarketEvent | None = None

    # Historical memory (unbounded for now; can be replaced by rolling window later)
    history: dict[str, list[float]] = field(default_factory=dict)
    features_history: dict[str, list[float]] = field(default_factory=dict)

    # Instantaneous computed features (at current step)
    features: dict[str, list[float]] = field(default_factory=dict)

    @property
    def timestamp(self) -> pd.Timestamp:
        if self.snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        return self.snapshot.timestamp

    @property
    def bar(self) -> OHLCV:
        if self.snapshot is None:
            raise ContextNotInitializedError("No MarketEvent processed yet")
        return self.snapshot.bar