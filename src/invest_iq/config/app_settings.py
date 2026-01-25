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

BASE_DIR = Path(r"D:\3 - InvestIQ-runs")
app_settings = AppSettings(
    base_dir=BASE_DIR,
    engine_log_dir=BASE_DIR / "Engine logs",
    backtest_log_dir=BASE_DIR / "Backtest logs",
    env=EnvType.PRODUCTION,
    debug=DebugMode.OFF,
)
