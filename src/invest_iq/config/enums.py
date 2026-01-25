from enum import Enum, auto


class EnvType(Enum):
    PRODUCTION=auto()
    DEBUG=auto()

class DebugMode(Enum):
    ON=auto()
    OFF=auto()