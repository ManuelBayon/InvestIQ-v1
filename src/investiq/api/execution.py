from collections.abc import Mapping
from dataclasses import dataclass, field

import pandas as pd

from investiq.api.instruments import InstrumentSpec
from investiq.execution.portfolio.types import Fill
from investiq.execution.transition.logs import TransitionLog


@dataclass(frozen=True)
class Decision:
    timestamp: pd.Timestamp
    target_position: float
    execution_price: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionView:
    current_position: float
    cash: float
    realized_pnl: float
    unrealized_pnl: float

@dataclass(frozen=True)
class RunResult:
    run_id: str
    instrument: InstrumentSpec
    start: pd.Timestamp
    end: pd.Timestamp
    metrics: Mapping[str, float]
    execution_log: list[Fill]
    transition_log: list[TransitionLog] = field(default_factory=tuple)
    diagnostics: Mapping[str, object] = field(default_factory=dict)