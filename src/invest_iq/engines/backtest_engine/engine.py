from invest_iq.common.market_types import MarketEvent
from invest_iq.engines.backtest_engine.common.backtest_context import BacktestContext
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
    ):
        self._logger = logger
        self._orchestrator = orchestrator
        self._transition_engine = transition_engine
        self.portfolio = portfolio

    def step(
            self,
            event: MarketEvent,
            context: BacktestContext,
    ) -> None:

        # 1. Read bar and timestamp
        context.snapshot = event

        # 2. Update history
        for k, v in context.snapshot.bar.items():
            context.history.setdefault(k, []).append(v)

        # 3. Run orchestrator
        orchestrator_out = self._orchestrator.run(context)
        context.model.orchestrator = orchestrator_out

        # 4. Adapt orchestrator signal to PortfolioSignal
        portfolio_signal = SignalAdapter.adapt(
            orchestrator_output=orchestrator_out,
        )

        # 5. Compute transition (delta position, trades, FIFO ops)
        transition_result = self._transition_engine.process(
            timestamp=portfolio_signal.timestamp,
            current_position=self.portfolio.current_position,
            target_position=portfolio_signal.target_position,
            price=portfolio_signal.price,
            fifo_queues=self.portfolio.fifo_queues,
        )

        # 6. Apply trades to portfolio
        self.portfolio.apply_operations(operations=transition_result)

        # 7. Update execution state
        context.execution.current_position = self.portfolio.current_position
        context.execution.cash = self.portfolio.cash
        context.execution.realized_pnl = self.portfolio.realized_pnl
        context.execution.unrealized_pnl = self.portfolio.unrealized_pnl
        context.execution.fifo_queues = self.portfolio.fifo_queues
        context.execution.execution_log = self.portfolio.execution_log