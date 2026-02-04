from dataclasses import dataclass
from pathlib import Path

from invest_iq.config.enums import EnvType, DebugMode


@dataclass
class AppSettings:
    base_dir: Path
    engine_log_dir: Path
    backtest_log_dir: Path
    env: EnvType
    debug: DebugMode
