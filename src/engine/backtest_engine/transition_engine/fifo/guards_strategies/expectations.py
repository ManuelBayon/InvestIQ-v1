from dataclasses import dataclass

from engine.backtest_engine.common.enums import AtomicActionType, FIFOSide


@dataclass(frozen=True)
class GuardExpectation:
    """Base expectations object for SafeGuards."""
    pass

@dataclass(frozen=True)
class ActionPriceExpectation(GuardExpectation):
    must_be_positive: bool = True

@dataclass(frozen=True)
class ActionQuantityExpectation(GuardExpectation):
    min_qty: float = 0.0

@dataclass(frozen=True)
class ActionTimestampExpectation(GuardExpectation):
    pass

@dataclass(frozen=True)
class ActionTypeExpectation(GuardExpectation):
    action_type: AtomicActionType

@dataclass(frozen=True)
class FIFOCapacityExpectation(GuardExpectation):
    side: FIFOSide
    required_qty: float
