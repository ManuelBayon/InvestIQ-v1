from typing import Callable

from invest_iq.engines.utilities.validator.protocol import ValidatorProtocol


class ValidatorRegistry:

    _registry: dict[str, Callable[..., ValidatorProtocol[object]]]

    @classmethod
    def register(
            cls,
            name: str
    ) -> None:
        ...