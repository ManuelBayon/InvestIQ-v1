from abc import ABC
from typing import ClassVar

from utilities.logger.protocol import LoggerProtocol, NullLogger


class TransitionRuleBase(ABC):
    """
        Defines a classification rule for transition_engine.
    """
    RULE_NAME: ClassVar[str]

    def __init__(
            self,
            logger: LoggerProtocol
    ) -> None:
        self._logger= logger