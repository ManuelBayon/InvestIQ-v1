from collections.abc import Mapping
from dataclasses import dataclass

import pandas as pd

from investiq.api.execution import Decision, ExecutionView
from investiq.api.market import MarketDataEvent
from investiq.execution.transition.types import FIFOOperation


@dataclass(frozen=True)
class StepRecord:
    timestamp: pd.Timestamp
    event: MarketDataEvent
    decision: Decision
    transition_result: list[FIFOOperation]
    execution_after: ExecutionView
    diagnostics: Mapping[str, object]