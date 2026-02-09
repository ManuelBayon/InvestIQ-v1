from dataclasses import dataclass

from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.planner import ExecutionPlan, OCO


@dataclass(frozen=True, slots=True)
class FixedPctOCOPlanner:
    """
    Attach fixed % SL/TP brackets to non-zero targets.

    Invariants:
    - sl_pct > 0 and tp_pct > 0
    - If target_position == 0: no brackets (oco=None)
    - If target_position > 0: SL below price, TP above price
    - If target_position < 0: SL above price, TP below price
    """
    sl_pct: float = 0.002
    tp_pct: float = 0.004

    def __post_init__(self) -> None:
        if self.sl_pct <= 0.0:
            raise ValueError("sl_pct must be > 0")
        if self.tp_pct <= 0.0:
            raise ValueError("tp_pct must be > 0")

    def plan(self, *, view: BacktestView, decision: Decision) -> ExecutionPlan:
        # `view` is unused for now, but kept for interface uniformity.
        px = float(decision.execution_price)
        tgt = float(decision.target_position)

        if tgt == 0.0:
            return ExecutionPlan(
                timestamp=decision.timestamp,
                target_position=0.0,
                execution_price=px,
                oco=None,
                diagnostics={},
            )

        if tgt > 0.0:
            oco = OCO(
                stop_loss=px * (1.0 - self.sl_pct),
                take_profit=px * (1.0 + self.tp_pct),
            )
        else:  # tgt < 0.0
            oco = OCO(
                stop_loss=px * (1.0 + self.sl_pct),
                take_profit=px * (1.0 - self.tp_pct),
            )

        return ExecutionPlan(
            timestamp=decision.timestamp,
            target_position=tgt,
            execution_price=px,
            oco=oco,
            diagnostics={},
        )