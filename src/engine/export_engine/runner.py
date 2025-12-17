from engine.backtest_engine.common.types import ExecutionLogEntry
from engine.export_engine.factory import ExportServiceFactory
from engine.export_engine.registries.config import ExportKey, ExportOptions

from engine.utilities.logger.factory import LoggerFactory


class BacktestExportRunner:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            export_key: ExportKey,
            export_options: ExportOptions,
    ):
        self._logger_factory = logger_factory
        self._export_key = export_key
        self._export_options = export_options


        self._export_service_factory = ExportServiceFactory(
            logger_factory=self._logger_factory,
            options=self._export_options,
        )

    def export_execution_log(
            self,
            execution_log: list[ExecutionLogEntry]
    ) -> None:

        export_service = self._export_service_factory.create_backtest_batch_export_service(
            key=self._export_key,
            logger_factory=self._logger_factory,
        )
        export_service.export(raw_data=execution_log)