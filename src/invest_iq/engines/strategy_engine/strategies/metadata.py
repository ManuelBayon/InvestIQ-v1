from dataclasses import dataclass

from invest_iq.engines.backtest_engine.common.types import MarketField, ComponentType


@dataclass(frozen=True)
class StrategyMetadata:
    strategy_uuid: str
    created_at: str
    name: str
    version: str
    description : str
    parameters: dict[str, object]
    price_type : MarketField
    required_fields : list[str]
    produced_features : list[str]
    component_type : ComponentType = ComponentType.STRATEGY