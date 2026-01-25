from typing import ClassVar

from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


class FIFOExecutionStrategyBase:

    STRATEGY_NAME: ClassVar[str]

    def __init__(
            self,
            logger: LoggerProtocol
    ) -> None:
        self._logger = logger