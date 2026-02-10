import pandas as pd

from investiq.api.backtest import BacktestView, BacktestInput
from investiq.api.execution import ExecutionView, RunResult
from investiq.api.market import MarketDataEvent
from investiq.core.execution_planner import ExecutionPlanner
from investiq.core.features.store import FeatureStore
from investiq.core.invariants import BacktestInvariantError
from investiq.core.market_state_builder import MarketStateBuilder
from investiq.utilities.logger.factory import LoggerFactory
from investiq.execution.portfolio.portfolio import Portfolio
from investiq.execution.transition.engine import TransitionEngine
from investiq.core.orchestrator import StrategyOrchestrator
from investiq.runs.audit import StepRecord


class BacktestEngine:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            strategy_orchestrator: StrategyOrchestrator,
            execution_planner: ExecutionPlanner,
            transition_engine: TransitionEngine,
            portfolio: Portfolio,
            market_store: MarketStateBuilder | None = None,
            feature_store: FeatureStore | None = None,
    ):
        self._logger = logger_factory.child("BacktestEngine").get()
        self._strategy_orchestrator = strategy_orchestrator
        self._execution_planner = execution_planner
        self._transition_engine = transition_engine
        self._portfolio = portfolio
        self._market = market_store or MarketStateBuilder()
        self._feature_store = feature_store or FeatureStore(logger=logger_factory.child("FeatureStore").get())

    def _execution_view(self) -> ExecutionView:
        return ExecutionView(
            current_position=self._portfolio.current_position,
            cash=self._portfolio.cash,
            realized_pnl=self._portfolio.realized_pnl,
            unrealized_pnl=self._portfolio.unrealized_pnl,
        )

    def step(
            self,
            event: MarketDataEvent,
    ) -> StepRecord:

        self._market.ingest(event=event)
        self._feature_store.ingest(market_store=self._market)

        # 1. Build read-only view
        view = BacktestView(
            market=self._market.view(),
            features=self._feature_store.view(),
            execution=self._execution_view(),
        )

        # 2. Run decision and planner pipeline
        decision = self._strategy_orchestrator.run(view=view)
        plan = self._execution_planner.plan(view=view, decision=decision)

        if plan.timestamp != view.market.timestamp:
            raise BacktestInvariantError("Decision timestamp must match market timestamp")

        # 4) Pure transition computation
        ops = self._transition_engine.process(
            plan=plan,
            current_position=view.execution.current_position,
            fifo_queues=self._portfolio.fifo_queues,
        )

        # 5) Mutate portfolio
        self._portfolio.apply_operations(ops)

        # 6. Immutable audit record
        exec_after = self._execution_view()
        return StepRecord(
            timestamp=view.market.timestamp,
            event=event,
            decision=decision,
            transition_result=ops,
            execution_after=exec_after,
            diagnostics=decision.diagnostics,
        )

    def run(self, bt_input: BacktestInput) -> RunResult:

        first_ts: pd.Timestamp | None = None
        last_ts: pd.Timestamp | None = None

        for event in bt_input.events:
            step_record = self.step(event)
            if first_ts is None:
                first_ts = step_record.timestamp
            last_ts = step_record.timestamp

        if first_ts is None or last_ts is None:
            raise BacktestInvariantError("No events provided")

        metrics = {
            "Realized PnL": float(self._portfolio.realized_pnl),
            "Unrealized PnL": float(self._portfolio.unrealized_pnl),
            "Final Cash": float(self._portfolio.cash),
            "Final Position": float(self._portfolio.current_position),
        }

        return RunResult(
            run_id="run_id",
            instrument=bt_input.instrument,
            start=first_ts,
            end=last_ts,
            metrics=metrics,
            execution_log=self._portfolio.execution_log,
            transition_log=[],
            diagnostics={}
        )

    @property
    def market_store(self) -> MarketStateBuilder:
        return self._market

    @property
    def portfolio(self) -> "Portfolio":
        return self._portfolio