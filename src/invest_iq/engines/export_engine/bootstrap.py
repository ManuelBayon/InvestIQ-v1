from invest_iq.engines.export_engine.registries.components.backtest import BacktestExportRegistry
from invest_iq.engines.export_engine.registries.config import ExportKey
from invest_iq.engines.utilities.import_tools import import_submodules
from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


def validate_export_registry(
        logger: LoggerProtocol,
) -> None:
    """
    Validate that all export bindings have been registered correctly.
    """

    # Force-load all modules that contain @bind declarations
    import_submodules("invest_iq.engines.export_engine.services.components")

    registered = set(BacktestExportRegistry.available())
    expected = set(e for e in ExportKey)

    missing = expected - registered
    extra = registered - expected

    if missing:
        raise RuntimeError(f"Missing export bindings: {missing}")
    if extra:
        raise RuntimeError(f"Unexpected export bindings: {extra}")

    logger.info(f"Backtest export bindings: {len(registered)} / {len(expected)} registered.")


def export_engine_bootstrap(
        logger: LoggerProtocol
) -> None:
    """
    Entry point for initializing and validating all export-related registries.
    """
    logger.info("Initializing export engines...")
    validate_export_registry(logger)
    logger.info("Export engines initialized successfully.")