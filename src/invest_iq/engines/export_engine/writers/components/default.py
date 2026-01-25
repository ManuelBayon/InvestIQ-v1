from typing import TypeVar

from invest_iq.engines.export_engine.writers.base_batch_writer import BatchWriter

FormattedT = TypeVar("FormattedT")
EncodedT = TypeVar("EncodedT")

class DefaultBatchWriter(BatchWriter[FormattedT, EncodedT]):
    """Concrete default implementation for most use-cases."""
    pass