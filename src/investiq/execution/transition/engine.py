from investiq.api.execution import Decision
from investiq.api.planner import ExecutionPlan
from investiq.execution.transition.fifo.resolver import FIFOResolver
from investiq.utilities.logger.factory import LoggerFactory
from investiq.execution.transition.enums import FIFOSide, TransitionType
from investiq.execution.transition.logs import TransitionLog
from investiq.execution.transition.rules.api import TransitionRule
from investiq.execution.transition.rules.classifier import compute_key
from investiq.execution.transition.rules.factory import TransitionRuleFactory
from investiq.execution.transition.strategies.api import TransitionStrategy
from investiq.execution.transition.strategies.factory import TransitionStrategyFactory
from investiq.execution.transition.types import FIFOPosition, FIFOOperation, AtomicAction


class TransitionEngine:

    def __init__(
            self,
            logger_factory: LoggerFactory,
    ) -> None:
        self._logger_factory : LoggerFactory = logger_factory
        self._logger = logger_factory.child("TransitionEngine").get()
        self._transition_rule_factory =  TransitionRuleFactory()
        self._transition_strategy_factory = TransitionStrategyFactory()
        self._fifo_resolver = FIFOResolver()
        self._last_resolution : TransitionLog | None = None

    def process(
            self,
            plan: ExecutionPlan,
            current_position : float,
            fifo_queues : dict[FIFOSide, list[FIFOPosition]],
    ) -> list[FIFOOperation]:

        # 1. Build context
        key = compute_key(
            current_position=current_position,
            target_position=plan.target_position
        )
        # 2. Get the transition rule and resolve transition
        rule: TransitionRule = self._transition_rule_factory.create(key=key)
        transition_type: TransitionType = rule.classify(
            current_position=current_position,
            target_position=plan.target_position
        )
        # 3. Get the transition strategy and resolve the atomic actions
        strategy : TransitionStrategy = self._transition_strategy_factory.create(
            transition_type=transition_type
        )
        atomic_actions: list[AtomicAction] = strategy.resolve(
            current_position=current_position,
            target_position=plan.target_position,
            timestamp=plan.timestamp
        )
        # 4. Resolve fifo operations
        fifo_operations: list[FIFOOperation] = self._fifo_resolver.resolve(
            actions=atomic_actions,
            fifo_queues=fifo_queues,
            execution_price=plan.execution_price
        )
        # 5.Build Audit Log
        log_entry = TransitionLog(
            state=key.state,
            event=key.event,
            current_position=current_position,
            target_position=plan.target_position,
            rule_name=rule.NAME,
            transition_strategy=strategy.NAME,
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
            log.transition_strategy,
            log.transition_type,
            log.actions_len,
            log.fifo_ops_len,
        )