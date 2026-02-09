from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.planner import ExecutionPlan

class NoBracketsPlanner:
    """
    Pure target execution (no SL/TP).
    """
    def plan(
            self,
            *,
            view: BacktestView,
            decision: Decision
    ) -> ExecutionPlan:
        return ExecutionPlan(
            timestamp=decision.timestamp,
            target_position=float(decision.target_position),
            execution_price=float(decision.execution_price),
            oco=None,
            diagnostics={},
        )