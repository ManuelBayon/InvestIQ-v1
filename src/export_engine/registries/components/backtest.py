from export_engine.registries.base import BaseBatchExportRegistry
from export_engine.registries.config import ExportKey, BatchExportBinding


class BacktestExportRegistry[RawT, FormattedT, EncodedT](BaseBatchExportRegistry[ExportKey,RawT, FormattedT, EncodedT]):
    """
    Concrete registry for backtest export pipelines.
    """
    @classmethod
    def register(
            cls,
            key: ExportKey,
            binding: BatchExportBinding[RawT, FormattedT, EncodedT]
    ) -> None:
        if key in cls._registry:
            raise KeyError(f"{key.value} already registered in {cls.__name__}")
        cls._registry[key] = binding

    @classmethod
    def get(
            cls,
            key: ExportKey
    ) -> BatchExportBinding[RawT, FormattedT, EncodedT]:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(
                f"{key.value} not registered in {cls.__name__}; "
                f"available={list(cls._registry.keys())}"
            )

    @classmethod
    def available(cls) -> list[ExportKey]:
        return list(cls._registry.keys())

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()