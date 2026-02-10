from collections.abc import Iterable
from dataclasses import dataclass

from investiq.api.execution import ExecutionView
from investiq.api.feature import FeatureSnapshot
from investiq.api.instruments import InstrumentSpec
from investiq.api.market import MarketDataEvent, MarketSate


@dataclass(frozen=True)
class BacktestInput:
    instrument: InstrumentSpec
    events: Iterable[MarketDataEvent]

@dataclass(frozen=True)
class BacktestView:
    """
    The ONLY object passed to strategies/orchestrator.
    Read-only contract: strategies cannot mutate the world.
    """
    market: MarketSate
    features: FeatureSnapshot
    execution: ExecutionView