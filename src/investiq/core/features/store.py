from collections import defaultdict
from collections.abc import Sequence

from typing import Final

from investiq.api.feature import FeatureView
from investiq.core.features.api import FeaturePipeline
from investiq.core.features.registry import FeaturePipelineRegistry
from investiq.core.market_store import MarketStore
from investiq.utilities.logger.protocol import LoggerProtocol


class FeatureStore:
    """
    Generic FeatureStore:
        - holds latest value and optional history
        - runs pipelines to compute / update features
    """

    def __init__(
            self,
            logger: LoggerProtocol,
            pipelines: Sequence[FeaturePipeline] | None = None,
            keep_history: bool = True,
    ):
        self._logger = logger
        self.keep_history: Final[bool] = keep_history
        self._values: dict[str, float] = {}
        self._history: dict[str, list[float]] = defaultdict(list)

        # 1. Build pipeline dict indexed by logical identity (NAME)
        if pipelines is None:
            pipeline_items = [(cls_.NAME, cls_()) for cls_ in FeaturePipelineRegistry.all()]
        else:
            pipeline_items = [(p.NAME, p) for p in pipelines]

        names = [name for name, _ in pipeline_items]
        if len(names) != len(set(names)):
            dup = sorted({n for n in names if names.count(n) > 1})
            raise ValueError(f"Duplicate pipeline NAME(s): {dup}")

        self._pipelines: dict[str, FeaturePipeline] = dict(pipeline_items)
        self._pipelines_ready: dict[str, bool] = {name: False for name in self._pipelines}

    def reset(self) -> None:
        """
        Reset stored values/history and reset pipelines + readiness.
        """
        self._values.clear()
        self._history.clear()
        for name in self._pipelines_ready:
            self._pipelines_ready[name] = False
        for p in self._pipelines.values():
            p.reset()

    def set_pipeline_ready(self, pipeline: str) -> None:
        """
        Mark a pipeline as ready for the current ingest step.

        Readiness is recomputed at each call to `ingest()`: all pipelines are first
        marked as not ready, then each pipeline sets its readiness during its
        `update()` execution if its outputs are valid for the current market state.
        """
        self._require_pipeline(pipeline)
        self._pipelines_ready[pipeline] = True

    def pipeline_ready(self, pipeline: str) -> bool:
        self._require_pipeline(pipeline)
        return self._pipelines_ready[pipeline]

    def global_ready(self) -> bool:
        """
        Global readiness: all pipelines warmed up.
        """
        # Neutral element: if no pipelines configured, consider store ready.
        return all(self._pipelines_ready.values()) if self._pipelines_ready else True

    def set_value(self, name: str, value: float) -> None:
        """
        Write/update a feature value (and history if enabled).
        This method is called from the FeaturePipeline.
        """
        v = float(value)
        self._values[name] = v
        if self.keep_history:
            self._history[name].append(v)

    def ingest(self, market_store: MarketStore) -> None:
        """
         Run all pipelines once for the given market snapshot.
         This method is called from the Strategy orchestrator.
        """
        self._pipelines_ready = {k: False for k in self._pipelines_ready}
        for p in self._pipelines.values():
            p.update(
                market_store=market_store,
                feature_store=self
            )

    def view(self, snapshot_history: bool = True) -> FeatureView:
        """
        Return a snapshot of current feature values, history, and readiness.
        If `snapshot_history` is True, history is copied as immutable tuples;
        otherwise the underlying history storage is returned by reference.
        """
        if snapshot_history:
            hist = {k: tuple(v) for k, v in self._history.items()}
        else:
            hist = self._history
        return FeatureView(
            values=dict(self._values),
            history=hist,
            pipeline_ready=dict(self._pipelines_ready),
            global_ready=self.global_ready()
        )

    def _require_pipeline(self, name: str) -> None:
        if name not in self._pipelines:
            raise KeyError(
                f"pipeline '{name}' not found in FeatureStore, "
                f"known={sorted(self._pipelines)}"
            )

    def pipeline_names(self) -> frozenset[str]:
        return frozenset(self._pipelines)