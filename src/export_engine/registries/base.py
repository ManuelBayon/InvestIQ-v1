from abc import ABC, abstractmethod
from typing import Callable

from export_engine.formatters.base_batch_formatter import BatchFormatter
from export_engine.registries.config import ExportKey, BatchExportBinding
from export_engine.sinks.base_batch_sink import BatchSink
from export_engine.writers_core.base_core_batch_writer import BatchWriterCore


class BaseBatchExportRegistry[KeyT: ExportKey, RawT, FormattedT, EncodedT](ABC):
    """
    Abstract registries enforcing a consistent API for all export binding registries.
    """
    _registry: dict[KeyT, BatchExportBinding[RawT, FormattedT, EncodedT]]

    def __init_subclass__(cls, **kwargs: object) -> None:
        """
        Each subclass must declare its own _registry to avoid collisions.
        """
        cls._registry = {}

    @classmethod
    @abstractmethod
    def register(cls, key: KeyT, binding: BatchExportBinding[RawT, FormattedT, EncodedT]) -> None:
        """Register a new export binding."""

    @classmethod
    @abstractmethod
    def get(cls, key: KeyT) -> BatchExportBinding[RawT, FormattedT, EncodedT]:
        """Retrieve a binding by key."""

    @classmethod
    @abstractmethod
    def available(cls) -> list[KeyT]:
        """List all registered keys."""

    @classmethod
    @abstractmethod
    def clear(cls) -> None:
        """Clear all registered bindings (used for tests)."""

    @classmethod
    def bind(
            cls,
            *,
            key: KeyT,
            raw: type[RawT],
            formatted: type[FormattedT],
            encoded: type[EncodedT],

    ) -> Callable[[type], type]:
        """
        Declarative decorator that registers a pipeline binding.

        Parameters
        ----------
        key : ExportKey
            Logical identifier of the export pipeline.
        raw : type[RawT]
            Raw data domain type (input of the formatter).
            Used only for static type resolution — not at runtime.
        formatted : type[FormattedT]
            Formatted data type (output of formatter, input of writer_core).
            Used for static validation of component compatibility.
        encoded : type[EncodedT]
            Encoded artifact type (output of writer_core, input of sink).
            Used for static type binding; never used at runtime.
        """

        def decorator(binding_cls: type) -> type:
            # --- Extract attributes ---
            fc = getattr(binding_cls, "formatter_cls", None)
            wc = getattr(binding_cls, "writer_core_cls", None)
            sc = getattr(binding_cls, "sink_cls", None)

            if fc is None or wc is None or sc is None:
                raise TypeError(
                    f"{binding_cls.__name__} must define formatter_cls, writer_core_cls, and sink_cls"
                )

            formatter_cls: type[BatchFormatter[RawT, FormattedT]] = fc
            writer_core_cls: type[BatchWriterCore[FormattedT, EncodedT]] = wc
            sink_cls: type[BatchSink[EncodedT]] = sc

            binding: BatchExportBinding[RawT, FormattedT, EncodedT] = BatchExportBinding(
                formatter_cls=formatter_cls,
                writer_core_cls=writer_core_cls,
                sink_cls=sink_cls,
            )

            cls.register(key, binding)
            return binding_cls

        return decorator