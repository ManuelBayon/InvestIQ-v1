from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PortfolioSignal:
    timestamp: datetime
    price: float
    target_position: float