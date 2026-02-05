from typing import Iterable

import pandas as pd

from investiq.execution.portfolio.types import Fill
from investiq.export_engine.formatters.base_batch_formatter import BatchFormatter
from investiq.utilities.logger.protocol import LoggerProtocol
from investiq.utilities.time_utils import format_utc_offset


class BacktestDataFrameFormatter(BatchFormatter[Fill, pd.DataFrame]):
    """
    Converts a list of ExecutionLogEntry into a clean, Excel-safe DataFrame.
    """
    def __init__(
            self,
            logger: LoggerProtocol
    ) -> None:
        super().__init__(logger)

    def _format(self, data: Iterable[Fill]) -> pd.DataFrame:
        rows = []
        for entry in data:
            ts = entry.timestamp
            timezone_str = format_utc_offset(ts)
            ts_naive = ts.replace(tzinfo=None)
            rows.append({
                "timestamp": ts_naive,
                "timezone": timezone_str,
                "operation_type": entry.operation_type.name,
                "side": entry.side.name,
                "quantity": entry.quantity,
                "entry_price": entry.entry_price,
                "pos_before": entry.position_before,
                "pos_after": entry.position_after,
                "exit_price": entry.exit_price,
                "realized_pnl": entry.realized_pnl,
                "parent_id": entry.linked_position_id,
            })

        df = pd.DataFrame(rows)
        self._logger.info(f"Formatted {len(df)} rows into DataFrame.")
        return df