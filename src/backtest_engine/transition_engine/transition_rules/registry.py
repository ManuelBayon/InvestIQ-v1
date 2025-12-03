from typing import TypeVar, Callable

from backtest_engine.common.enums import CurrentState, Event
from backtest_engine.transition_engine.transition_rules.interface import TransitionRule


class TransitionRuleRegistry:

    _registry : dict[tuple[CurrentState, Event], type[TransitionRule]] = {}

    @classmethod
    def register(
            cls,
            state : CurrentState,
            event : Event,
            rule_cls: type[TransitionRule]
    ) -> None:
        key = (state, event)
        if key in cls._registry:
            raise KeyError(f"Rule for {key} already registered")
        cls._registry[key] = rule_cls

    @classmethod
    def get(
            cls,
            key : tuple[CurrentState, Event]
    ) -> type[TransitionRule]:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(
                f"Transition: {key} is not supported"
                f"Available transitions: {cls.available()}"
            )

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()

    @classmethod
    def available(cls) -> list[tuple[CurrentState, Event]]:
        return list(cls._registry.keys())

###################################################################
###                           Decorator                         ###
###################################################################
T = TypeVar("T", bound=TransitionRule)
def register_transition_rule(
        state: CurrentState,
        event: Event
) -> Callable[[type[T]], type[T]]:

    def decorator(rule_cls: type[T]) -> type[T]:
        TransitionRuleRegistry.register(
            state=state,
            event=event,
            rule_cls=rule_cls)
        return rule_cls

    return decorator