from dash import Dash, html, dcc, Output, Input
import plotly.graph_objects as go

from backtest_engine.common.enums import FutureCME
from backtest_engine.factory import build_backtest
from backtest_engine.orchestrator import BacktestOrchestrator
from historical_data_engine.enums import BarSize
from strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy
from utilities.logger.factory import LoggerFactory
from utilities.logger.setup import init_base_logger

# 1. Logger
init_base_logger(debug=True)
logger_factory = LoggerFactory(
    engine_type="GUI",
    run_id="test_gui",
)

bundle = build_backtest(
    logger_factory=logger_factory,
    symbol=FutureCME.MNQ,
    duration_setting="100 D",
    bar_size_setting=BarSize.ONE_HOUR,
    strategy=MovingAverageCrossStrategy,
    filters=None,
    initial_cash=100_000,
)

orchestrator = BacktestOrchestrator(
    engine=bundle.engine,
    context=bundle.context,
)

candles = list(orchestrator.stream_candles(bt_input=bundle.input))

# 2. Dash app
app = Dash(__name__)

app.layout = html.Div(
style={"width": "95%", "margin": "auto"},
    children=[
        html.H2("InvestIQ – Backtest Candles"),

        dcc.Slider(
            id="time-slider",
            min=1,
            max=len(candles),
            step=1,
            value=min(50, len(candles)),
            tooltip={"placement": "bottom", "always_visible": True},
        ),

        dcc.Graph(id="candles-chart"),
    ],
)

# 3. Callback

@app.callback(
    Output("candles-chart", "figure"),
    Input("time-slider", "value"),
)
def update_chart(n):
    visible = candles[:n]

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=[c.timestamp for c in visible],
                open=[c.open for c in visible],
                high=[c.high for c in visible],
                low=[c.low for c in visible],
                close=[c.close for c in visible],
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)





