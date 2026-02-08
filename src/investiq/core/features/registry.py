from typing import TypeVar

from investiq.core.features.api import FeaturePipeline

T = TypeVar('T', bound='FeaturePipeline')

class FeaturePipelineRegistry:

    _registry: dict[str, type[FeaturePipeline]] = {}

    @classmethod
    def register(cls, pipeline_cls: type[FeaturePipeline]) -> None:
        name = getattr(pipeline_cls, "NAME", None)
        if not isinstance(name, str) or not name:
            raise TypeError(f"{pipeline_cls.__name__}.NAME must be a non-empty str")
        if name in cls._registry:
            raise KeyError(f"FeaturePipeline {name} already registered")
        cls._registry[name] = pipeline_cls

    @classmethod
    def get(cls, name: str) -> type[FeaturePipeline]:
        try:
            return cls._registry[name]
        except KeyError as e:
            raise KeyError(
                f"FeaturePipeline {name} not registered. "
                f"Available pipelines: {list(cls._registry)}"
            ) from e

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._registry)


def register_feature_pipeline(cls: type[T]) -> type[T]:
    FeaturePipelineRegistry.register(pipeline_cls=cls)
    return cls