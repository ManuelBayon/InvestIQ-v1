from enum import Enum, auto

class TransitionType(Enum):
    NO_OP = auto()
    OPEN_LONG = auto()
    INCREASE_LONG = auto()
    REDUCE_LONG = auto()
    CLOSE_LONG = auto()
    REVERSAL_TO_SHORT = auto()
    OPEN_SHORT = auto()
    INCREASE_SHORT = auto()
    REDUCE_SHORT = auto()
    CLOSE_SHORT = auto()
    REVERSAL_TO_LONG = auto()

class AtomicActionType(Enum):
    OPEN_LONG = auto()
    CLOSE_LONG = auto()
    OPEN_SHORT = auto()
    CLOSE_SHORT = auto()

class FIFOOperationType(Enum):
    CLOSE = auto()
    OPEN = auto()

class FIFOSide(Enum):
    LONG = auto()
    SHORT = auto()

class CurrentState(Enum):
    FLAT = auto()
    LONG = auto()
    SHORT = auto()

class Event(Enum):
    GO_FLAT = auto()
    GO_SHORT = auto()
    GO_LONG = auto()

class FutureCME(Enum):
    MNQ = "MNQ"
    MES = "MES"

class GuardName(str, Enum):
    ACTION_PRICE = "ActionPriceGuard"
    ACTION_QUANTITY = "ActionQuantityGuard"
    ACTION_TIMESTAMP = "ActionTimestampGuard"
    ACTION_TYPE = "ActionTypeGuard"
    FIFO_CAPACITY = "FifoCapacityGuard"