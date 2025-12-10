from backtest_engine.common.contracts import BacktestInput, BacktestContext
from backtest_engine.portfolio.portfolio import Portfolio
from backtest_engine.transition_engine.engine import TransitionEngine
from strategy_engine.orchestrator.adapters.signal_adapter import SignalAdapter
from strategy_engine.orchestrator.orchestrator import StrategyOrchestrator
from utilities.logger.factory import LoggerFactory

class BacktestEngine:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            orchestrator: StrategyOrchestrator,
            transition_engine: TransitionEngine,
            initial_cash : float = 100_000,
    ):
        self._logger = logger_factory.child("Backtest Engine").get()
        self._orchestrator = orchestrator
        self._transition_engine = transition_engine
        self.portfolio: Portfolio = Portfolio(
            logger_factory=logger_factory,
            transition_engine=transition_engine,
            initial_cash=initial_cash
        )

    def step(
            self,
            bt_input: BacktestInput,
            context: BacktestContext,
            i:int
    ) -> None:

        # 1. Read current candle
        context.timestamp = bt_input.timestamp.iloc[i]
        context.bar = {k: v.iloc[i] for k, v in bt_input.data.items()}

        # 2.Update history
        for k, v in context.bar.items():
            context.history[k].append(v)

        # 3. Strategy execution (raw signal + features)
        orchestrator_out = self._orchestrator.run(context)
        context.model.orchestrator = orchestrator_out

        # 4. Adapt signals to PortfolioSignal
        portfolio_signal = SignalAdapter.adapt(

        )