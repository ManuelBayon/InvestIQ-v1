from abc import ABC, abstractmethod

from dataclasses import dataclass

from invest_iq.engines.backtest_engine.common.types import BacktestView, Decision

@dataclass(frozen=True)
class FilterMetadata:
    filter_uuid: str
    created_at: str
    name: str
    version: str
    description: str
    parameters: dict[str, object]
    required_fields : list[str]
    produced_features: list[str]
    diagnostics_schema: list[str]

class AbstractFilter(ABC):
    metadata: FilterMetadata | None = None
    @abstractmethod
    def apply(
            self,
            view: BacktestView,
            decision: Decision,
    ) -> Decision:
        ...