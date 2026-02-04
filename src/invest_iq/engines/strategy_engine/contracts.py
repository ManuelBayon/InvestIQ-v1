from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pandas as pd

from invest_iq.engines.backtest_engine.common.backtest_context import OHLCV
from invest_iq.engines.strategy_engine.enums import MarketField
from invest_iq.engines.strategy_engine.strategies.metadata import StrategyMetadata

