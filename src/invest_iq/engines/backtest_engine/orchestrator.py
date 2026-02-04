from invest_iq.engines.backtest_engine.common.backtest_context import BacktestContext
from invest_iq.engines.backtest_engine.common.contracts import BacktestInput, BacktestResult
from invest_iq.engines.backtest_engine.engine import BacktestEngine
from invest_iq.engines.utilities.logger.factory import LoggerFactory


class BacktestRunner:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            engine: BacktestEngine,
            context: BacktestContext,
    ):
        self._logger_factory = logger_factory
        self._engine = engine
        self._context = context

    def run(
            self,
            bt_input: BacktestInput
    ) -> BacktestResult:

        for event in bt_input.events:
            self._engine.step(
               event=event,
               context=self._context,
            )

        p = self._engine.portfolio

        return BacktestResult(
            execution_log=p.execution_log,
            final_cash=p.cash,
            realized_pnl=p.realized_pnl,
            unrealized_pnl=p.unrealized_pnl,
            diagnostics={}
        )