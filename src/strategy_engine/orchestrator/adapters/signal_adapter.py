from backtest_engine.portfolio.contracts import PortfolioSignal
from strategy_engine.strategies.contracts import OrchestratorOutput


class SignalAdapter:

    @staticmethod
    def adapt(orchestrator_output: OrchestratorOutput) -> list[PortfolioSignal]:
        return [
            PortfolioSignal(
                timestamp=ts,
                target_position=tp,
                price=price
            )
            for ts, tp, price in zip(
                orchestrator_output.timestamp,
                orchestrator_output.target_position,
                orchestrator_output.price_serie
            )
        ]