from enum import StrEnum


class Version(StrEnum):
    V1= "1.0"

class MarketField(StrEnum):
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"

class ComponentType(StrEnum):
    STRATEGY = "strategy"
    FILTER = "filter"