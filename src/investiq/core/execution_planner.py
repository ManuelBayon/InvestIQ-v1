
from typing import Protocol

from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.planner import ExecutionPlan

class ExecutionPlanner(Protocol):
    """
    Turn a Decision into an ExecutionPlan.
    """
    def plan(
            self,
            *,
            view: BacktestView,
            decision: Decision
    ) -> ExecutionPlan:
        ...