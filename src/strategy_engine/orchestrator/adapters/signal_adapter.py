from backtest_engine.portfolio.contracts import PortfolioSignal
from strategy_engine.contracts import OrchestratorOutput


class SignalAdapter:

    @staticmethod
    def adapt(orchestrator_output: OrchestratorOutput) -> PortfolioSignal:

            return PortfolioSignal(
                timestamp=orchestrator_output.timestamp,
                target_position=orchestrator_output.target_position,
                price=orchestrator_output.price
            )