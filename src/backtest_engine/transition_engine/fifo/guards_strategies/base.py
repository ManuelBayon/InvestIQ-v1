from abc import ABC, ABCMeta
from typing import ClassVar

from utilities.logger.protocol import LoggerProtocol


class SafeGuardBase(ABC):

    STRATEGY_NAME: ClassVar[str]

    def __init__(
            self,
            logger: LoggerProtocol
    ) -> None:
        self._logger= logger