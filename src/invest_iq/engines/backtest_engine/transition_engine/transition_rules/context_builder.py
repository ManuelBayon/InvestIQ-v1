from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event


class TransitionRuleContextBuilder:

    @staticmethod
    def build(
            current_position : float,
            target_position : float
    ) -> tuple[CurrentState, Event]:

        if current_position > 0:
            current_state = CurrentState.LONG
        elif current_position < 0:
            current_state = CurrentState.SHORT
        elif current_position == 0:
            current_state = CurrentState.FLAT
        else:
            raise ValueError(f"Invalid current_position: {current_position}")

        if target_position > 0:
            event = Event.GO_LONG
        elif target_position < 0:
            event = Event.GO_SHORT
        elif target_position == 0:
            event = Event.GO_FLAT
        else:
            raise ValueError(f"Invalid target_position: {target_position}")

        return current_state, event