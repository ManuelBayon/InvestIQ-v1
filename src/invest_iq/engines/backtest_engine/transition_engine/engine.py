from datetime import datetime
from typing import Optional

from invest_iq.engines.backtest_engine.common.enums import FIFOSide, TransitionType
from invest_iq.engines.backtest_engine.common.types import AtomicAction, TransitionLog, FIFOPosition, FIFOOperation

from invest_iq.engines.backtest_engine.transition_engine.fifo.resolver import FIFOResolver
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.factory import TransitionRuleFactory
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.context_builder import \
    TransitionRuleContextBuilder
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.interface import TransitionRule
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.factory import TransitionStrategyFactory
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from invest_iq.engines.utilities.logger.factory import LoggerFactory

class TransitionEngine:

    def __init__(
            self,
            logger_factory: LoggerFactory,
    ) -> None:
        self._logger_factory : LoggerFactory = logger_factory
        self._logger = logger_factory.child("TransitionEngine").get()
        self._transition_rule_factory =  TransitionRuleFactory(self._logger_factory)
        self._transition_strategy_factory = TransitionStrategyFactory(self._logger_factory)
        self._fifo_resolver : FIFOResolver = FIFOResolver(self._logger_factory)
        self._last_resolution : Optional[TransitionLog] = None

    def process(
            self,
            timestamp : datetime,
            current_position : float,
            target_position : float,
            price : float,
            fifo_queues : dict[FIFOSide, list[FIFOPosition]],
    ) -> list[FIFOOperation]:

        # 1. Build context
        state, event = TransitionRuleContextBuilder().build(
            current_position=current_position,
            target_position=target_position
        )
        # 2. Get the transition rule and resolve transition
        rule: TransitionRule = self._transition_rule_factory.create(
            state=state,
            event=event
        )
        transition_type: TransitionType = rule.classify(
            current_position=current_position,
            target_position=target_position
        )
        # 3. Get the transition strategy and resolve the atomic actions
        strategy : TransitionStrategy = self._transition_strategy_factory.create(
            transition_type=transition_type
        )
        atomic_actions: list[AtomicAction] = strategy.resolve(
            current_position=current_position,
            target_position=target_position,
            timestamp=timestamp
        )
        # 4. Resolve fifo operations
        fifo_operations: list[FIFOOperation] = self._fifo_resolver.resolve(
            actions=atomic_actions,
            fifo_queues=fifo_queues,
            execution_price=price
        )
        # 5.Build Audit Log
        log_entry = TransitionLog(
            state=state,
            event=event,
            current_position=current_position,
            target_position=target_position,
            rule_name=rule.RULE_NAME,
            strategy_name=strategy.STRATEGY_NAME,
            transition_type=transition_type.name,
            actions_len=len(atomic_actions),
            fifo_ops_len=len(fifo_operations)
        )
        if log_entry != self._last_resolution:
            self._log_operation(log=log_entry)
            self._last_resolution = log_entry
        # 6. Return the FIFOOperation list
        return fifo_operations

    def _log_operation(
            self,
            log : TransitionLog
    ) -> None:
        self._logger.debug(
            (
                "state=%s event=%s "
                "current=%.2f target=%.2f "
                "rule=%s strategy=%s "
                "transition=%s "
                "actions=%d fifo_ops=%d"
            ),
            log.state.name,
            log.event.name,
            log.current_position,
            log.target_position,
            log.rule_name,
            log.strategy_name,
            log.transition_type,
            log.actions_len,
            log.fifo_ops_len,
        )