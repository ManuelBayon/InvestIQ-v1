import pandas as pd

from invest_iq.engines.backtest_engine.common.errors import BacktestInvariantError
from invest_iq.engines.backtest_engine.common.types import MarketStore, ExecutionView, MarketEvent, BacktestView, \
    StepRecord, BacktestInput, RunResult
from invest_iq.engines.backtest_engine.portfolio.portfolio import Portfolio

from invest_iq.engines.backtest_engine.transition_engine.engine import TransitionEngine
from invest_iq.engines.strategy_engine.orchestrator import StrategyOrchestrator

from invest_iq.engines.utilities.logger.protocol import LoggerProtocol

class BacktestEngine:

    def __init__(
            self,
            logger: LoggerProtocol,
            strategy_orchestrator: StrategyOrchestrator,
            transition_engine: TransitionEngine,
            portfolio: Portfolio,
            market_store: MarketStore | None = None,
    ):
        self._logger = logger
        self._strategy_orchestrator = strategy_orchestrator
        self._transition_engine = transition_engine
        self._portfolio = portfolio
        self._market = market_store or MarketStore()

    def _execution_view(self) -> ExecutionView:
        return ExecutionView(
            current_position=self._portfolio.current_position,
            cash=self._portfolio.cash,
            realized_pnl=self._portfolio.realized_pnl,
            unrealized_pnl=self._portfolio.unrealized_pnl,
        )

    def step(
            self,
            event: MarketEvent,
    ) -> StepRecord:

        self._market.ingest(event)
        market_view = self._market.view()

        # 1. Build read-only view
        view = BacktestView(
            market=market_view,
            execution=self._execution_view(),
        )

        # 2. Run decision pipeline
        decision = self._strategy_orchestrator.run(view)

        if decision.timestamp != view.market.timestamp:
            raise BacktestInvariantError("Decision timestamp must match market timestamp")

        # 4) Pure transition computation
        ops = self._transition_engine.process(
            decision=decision,
            current_position=view.execution.current_position,
            fifo_queues=self._portfolio.fifo_queues,
        )

        # 5) Mutate portfolio
        self._portfolio.apply_operations(ops)

        # 6. Immutable audit record
        exec_after = self._execution_view()
        return StepRecord(
            timestamp=market_view.timestamp,
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
            "Final Cash": float(self._portfolio.cash),
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
    def market_store(self) -> MarketStore:
        return self._market

    @property
    def portfolio(self) -> "Portfolio":
        return self._portfolio