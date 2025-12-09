import pandas as pd

from backtest_engine.portfolio.portfolio import Portfolio
from backtest_engine.transition_engine.engine import TransitionEngine
from config.AppSettings import app_settings

from export_engine.factory import ExportServiceFactory
from export_engine.registries.config import ExportKey, ExportOptions

from historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from strategy_engine.strategies.contracts import OrchestratorInput, OrchestratorOutput
from strategy_engine.strategy_orchestrator import StrategyOrchestrator
from utilities.logger.factory import LoggerFactory


class BacktestEngine:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            hist_data_engine: HistoricalDataEngine,
            orchestrator: StrategyOrchestrator,
            transition_engine: TransitionEngine
    ):
        self._logger_factory = logger_factory.child("Backtest Engine")
        self._hist_data_engine = hist_data_engine
        self._orchestrator= orchestrator
        self._transition_engine = transition_engine
        self.portfolio: Portfolio = Portfolio(
            logger_factory=self._logger_factory.child("Portfolio"),
            transition_engine=self._transition_engine,
            initial_cash=100_000
        )
        self._data : pd.DataFrame
        self._orchestrator_output: OrchestratorOutput

    def _load_data(self) -> None:
        self._data = self._hist_data_engine.load_data()

    def _generate_signals(self) -> None:
        self._orchestrator_output = self._orchestrator.run(
            input_= OrchestratorInput(
                timestamp=self._data["timestamp"],
                data={
                    "open": self._data.open,
                    "high": self._data.high,
                    "low": self._data.low,
                    "close": self._data.close,
                },
                extra={}
            )
        )

    def _run_portfolio(self) -> None:
        self.portfolio.generate_and_apply_fifo_operations_from_signals(
            signals=pd.DataFrame({
                "timestamp": self._orchestrator_output.timestamp,
                "close": self._orchestrator_output.price_serie,
                "target_position": self._orchestrator_output.target_position
            }),
        )

    def export_logs(self) -> None:
        backtest_dir = app_settings.backtest_log_dir
        filename = "output"
        export_options: ExportOptions = ExportOptions(
            sink={
                "output_dir": backtest_dir,
                "filename": filename
            }
        )
        factory: ExportServiceFactory = ExportServiceFactory(
            logger_factory=self._logger_factory,
            options=export_options
        )
        export_service = factory.create_backtest_batch_export_service(ExportKey.EXCEL)
        export_service.export(self.portfolio.execution_log)
        print(f"Realized PnL : {self.portfolio.realized_pnl}")

    def run(self) -> None:
        self._load_data()
        self._generate_signals()
        self._run_portfolio()
        self.export_logs()