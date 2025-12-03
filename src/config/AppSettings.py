from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

class EnvType(Enum):
    PRODUCTION=auto()
    DEBUG=auto()

class DebugMode(Enum):
    ON=auto()
    OFF=auto()

@dataclass
class AppSettings:
    base_dir: Path
    engine_log_dir: Path
    backtest_log_dir: Path
    env: EnvType
    debug: DebugMode

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app_settings = AppSettings(
    base_dir=BASE_DIR,
    engine_log_dir  = BASE_DIR / "Engine Logs",
    backtest_log_dir= BASE_DIR / "Backtest Logs",
    debug=DebugMode.ON,
    env=EnvType.DEBUG,
)
