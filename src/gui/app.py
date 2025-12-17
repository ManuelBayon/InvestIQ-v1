# 1. Logger
from dash import Dash, html, dcc, Output, Input

from engine.backtest_engine.orchestrator import BacktestOrchestrator
from engine.utilities.logger.factory import LoggerFactory
from engine.utilities.logger.setup import init_base_logger
from experiments.mnq_ma_cross import build_experiment

import plotly.graph_objects as go

init_base_logger(debug=True)
logger_factory = LoggerFactory(
    engine_type="gui",
    run_id="test_gui",
)

# 2. Build bundle and initialize orchestrator
bundle = build_experiment(
    logger_factory=logger_factory
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





