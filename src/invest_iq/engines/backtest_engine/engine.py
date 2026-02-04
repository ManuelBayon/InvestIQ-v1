from collections.abc import Mapping

from invest_iq.engines.backtest_engine.common.types import MarketStore, ExecutionView, MarketEvent, BacktestView, \
    StepRecord
from invest_iq.engines.backtest_engine.portfolio.portfolio import Portfolio

from invest_iq.engines.backtest_engine.transition_engine.engine import TransitionEngine
from invest_iq.engines.strategy_engine.orchestrator.adapters.signal_adapter import SignalAdapter
from invest_iq.engines.strategy_engine.orchestrator.orchestrator import StrategyOrchestrator

from invest_iq.engines.utilities.logger.protocol import LoggerProtocol

class BacktestEngine:

    def __init__(
            self,
            logger: LoggerProtocol,
            orchestrator: StrategyOrchestrator,
            transition_engine: TransitionEngine,
            portfolio: Portfolio,
            market_store: MarketStore | None = None,
    ):
        self._logger = logger
        self._orchestrator = orchestrator
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

        # 1. Mutate MarketStore
        self._market.ingest(event)
        market_view = self._market.view()

        # 2. Build read-only backtest view for orchestrator / strategies
        view = BacktestView(
            market=market_view,
            execution=self._execution_view(),
        )

        # 3. Pure computation
        orchestrator_out = self._orchestrator.run(view)

        # 4. Pure adaptation
        portfolio_signal = SignalAdapter.adapt(orchestrator_out)

        # 5. Pure transition computation
        transition_result = self._transition_engine.process(
            timestamp=portfolio_signal.timestamp,
            current_position=self._portfolio.current_position,
            target_position=portfolio_signal.target_position,
            price=portfolio_signal.price,
            fifo_queues=self._portfolio.fifo_queues,
        )

        # 6. Mutate portfolio
        self._portfolio.apply_operations(transition_result)

        # 7. Immutable audit record
        exec_after = self._execution_view()
        return StepRecord(
            timestamp=market_view.timestamp,
            event=event,
            orchestrator_output=orchestrator_out,
            transition_result=transition_result,
            execution_after=exec_after,
            diagnostics=orchestrator_out.diagnostics,
        )

    @property
    def market_store(self) -> MarketStore:
        return self._market

    @property
    def portfolio(self) -> "Portfolio":
        return self._portfolio