from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

@dataclass(frozen=True)
class OCO:
    """
    One-Cancels-Other bracket: stop loss and take profit.
    """
    stop_loss: float | None = None
    take_profit: float | None = None


@dataclass(frozen=True)
class ExecutionPlan:
    """
    Execution-ready representation of a decision.
    """
    timestamp: pd.Timestamp
    target_position: float
    execution_price: float
    oco: OCO | None = None
    diagnostics: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class PlannerMetadata:
    """
    Metadata for execution planners (audit/repro).
    """
    name: str
    version: str
    parameters: Mapping[str, object] = field(default_factory=dict)
    component_type: str = "EXECUTION_PLANNER"
    created_at: datetime = field(default_factory=datetime.now)