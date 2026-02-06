from collections.abc import Iterable
from dataclasses import dataclass

from investiq.api.execution import ExecutionView
from investiq.api.feature import FeatureView
from investiq.api.instruments import InstrumentSpec
from investiq.api.market import MarketEvent, MarketView


@dataclass(frozen=True)
class BacktestInput:
    instrument: InstrumentSpec
    events: Iterable[MarketEvent]

@dataclass(frozen=True)
class BacktestView:
    """
    The ONLY object passed to strategies/orchestrator.
    Read-only contract: strategies cannot mutate the world.
    """
    market: MarketView
    features: FeatureView
    execution: ExecutionView