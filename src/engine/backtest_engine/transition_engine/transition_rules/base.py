from abc import ABC
from typing import ClassVar

from engine.utilities.logger.protocol import LoggerProtocol


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