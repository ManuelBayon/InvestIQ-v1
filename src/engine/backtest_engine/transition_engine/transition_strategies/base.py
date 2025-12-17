from abc import ABC
from typing import ClassVar

from engine.utilities.logger.protocol import LoggerProtocol


class TransitionStrategyBase(ABC):
    """

    """
    STRATEGY_NAME: ClassVar[str]

    def __init__(
            self,
            logger: LoggerProtocol
    ):
        self._logger= logger