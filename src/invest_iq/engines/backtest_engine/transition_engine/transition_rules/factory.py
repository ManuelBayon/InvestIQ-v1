from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.registry import TransitionRuleRegistry
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.interface import TransitionRule
from invest_iq.engines.utilities.logger.factory import LoggerFactory


class TransitionRuleFactory:

    CLASS_NAME: ClassVar[str] = "TransitionRuleFactory"

    def __init__(
            self,
            logger_factory: LoggerFactory,
    ) -> None:
        self._logger_factory: LoggerFactory = logger_factory

    def create(
            self,
            state  : CurrentState,
            event : Event
    ) -> TransitionRule:

        rule_cls: type[TransitionRule] = TransitionRuleRegistry.get((state, event))
        return rule_cls(
            logger=self._logger_factory.child(f"{rule_cls.RULE_NAME}").get()
        )