from dataclasses import dataclass

from investiq.execution.transition.enums import CurrentState, Event


@dataclass(frozen=True)
class TransitionLog:
    state: CurrentState
    event: Event
    current_position: float
    target_position: float
    rule_name: str
    transition_strategy: str
    transition_type: str
    actions_len: int
    fifo_ops_len: int
