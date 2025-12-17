from typing import TypeVar, Callable

from engine.utilities.import_tools import import_submodules
from engine.utilities.logger.protocol import LoggerProtocol

T = TypeVar("T")
def validate_registry(
        logger: LoggerProtocol,
        name: str,
        import_path: str,
        expected: set[T],
        available_fn: Callable[[], list[T]]
) -> None:
    """
    Generic validation for a registries:
    - Import modules from a path (to trigger registrations)
    - Check that available matches expected
    - Log summary, raises if mismatch
    """
    import_submodules(import_path)

    registered: set[T] = set(available_fn())
    missing = expected - registered
    extra = registered - expected

    if missing:
        raise RuntimeError(f"Missing {name}: {missing}")
    if extra:
        raise RuntimeError(f"Unexpected {name}: {extra}")

    logger.info(f"{name} registered: {len(registered)} / {len(expected)}")