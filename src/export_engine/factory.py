import inspect
from typing import TypeVar

from export_engine.formatters.base_batch_formatter import BatchFormatter
from export_engine.registries.components.backtest import BacktestExportRegistry
from export_engine.registries.config import ExportKey, BatchExportBinding, ExportOptions
from export_engine.services.batch_export_service import BatchExportService
from export_engine.sinks.base_batch_sink import BatchSink
from export_engine.writers.components.default import DefaultBatchWriter
from export_engine.writers_core.base_core_batch_writer import BatchWriterCore
from utilities.logger.factory import LoggerFactory
from utilities.logger.protocol import LoggerProtocol

RawT = TypeVar("RawT")
FormattedT = TypeVar("FormattedT")
EncodedT = TypeVar("EncodedT")

ClassT = TypeVar("ClassT")

class ExportServiceFactory:
    """
    Factory to assemble complete export pipelines from registry bindings.
    """
    def __init__(
            self,
            logger_factory: LoggerFactory,
            options: ExportOptions
    ):
        self._logger_factory = logger_factory
        self._logger: LoggerProtocol = self._logger_factory.child("ExportServiceFactory").get()
        self._options = options

    # Smart init
    @staticmethod
    def _instantiate(
            cls: type[ClassT],
            **overrides: object
    ) -> ClassT:
        """
        Safely instantiate a class, injecting only valid parameters.
        """
        signature = inspect.signature(cls) # Returns a dict of the constructor's signature
        valid_kwargs = {k: v for k, v in overrides.items() if k in signature.parameters}
        return cls(**valid_kwargs)


    def create_backtest_batch_export_service(
            self,
            key: ExportKey,
    ) -> BatchExportService[RawT, FormattedT, EncodedT]:
        """
        Build a BatchExportService dynamically from registry metadata.
        """
        self._logger.debug(f"Building export service for {key.value}")

        # Step 1 - Retrieve the binding from the registry
        binding: BatchExportBinding[object, object, object] = BacktestExportRegistry.get(key)

        # Step 2 - Instantiate components
        formatter: BatchFormatter[RawT, FormattedT] = self._instantiate(
            cls=binding.formatter_cls,
            logger=self._logger_factory.child("Formatter").get(),
            **self._options.formatter
        )
        writer_core: BatchWriterCore[FormattedT, EncodedT] = self._instantiate(
            cls=binding.writer_core_cls,
            logger=self._logger_factory.child("WriterCore").get(),
            **self._options.writer_core
        )
        sink: BatchSink[EncodedT] = self._instantiate(
            binding.sink_cls,
            logger=self._logger_factory.child("Sink").get(),
            **self._options.sink
        )
        writer_cls = binding.writer_cls or DefaultBatchWriter
        writer = writer_cls(
            logger=self._logger_factory.child("Batch Writer").get(),
            writer_core=writer_core,
            sink=sink,
        )

        # Step 3 - Return the Batch Export Service
        return BatchExportService(
            logger=self._logger_factory.child("Batch Export Service").get(),
            formatter=formatter,
            writer=writer
        )