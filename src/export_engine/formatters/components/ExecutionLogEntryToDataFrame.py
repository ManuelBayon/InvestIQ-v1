from typing import Iterable

import pandas as pd

from backtest_engine.common.types import ExecutionLogEntry
from export_engine.formatters.base_batch_formatter import BatchFormatter
from utilities.logger.protocol import LoggerProtocol


class BacktestDataFrameFormatter(BatchFormatter[ExecutionLogEntry, pd.DataFrame]):
    """
    Converts a list of ExecutionLogEntry into a clean, Excel-safe DataFrame.
    """
    def __init__(
            self,
            logger: LoggerProtocol
    ) -> None:
        super().__init__(logger)

    def _format(self, data: Iterable[ExecutionLogEntry]) -> pd.DataFrame:
        rows = []
        for entry in data:
            rows.append({
                "timestamp": entry.timestamp.replace(tzinfo=None) if entry.timestamp.tzinfo else entry.timestamp,
                "timezone": entry.timestamp.tzinfo.tzname(None) if entry.timestamp.tzinfo else "naive",
                "operation_type": entry.operation_type.name,
                "side": entry.side.name,
                "quantity": entry.quantity,
                "entry_price": entry.entry_price,
                "pos_before": entry.pos_before,
                "pos_after": entry.pos_after,
                "exit_price": entry.exit_price,
                "realized_pnl": entry.realized_pnl,
                "parent_id": entry.parent_id,
            })

        df = pd.DataFrame(rows)
        self._logger.info(f"Formatted {len(df)} rows into DataFrame.")
        return df