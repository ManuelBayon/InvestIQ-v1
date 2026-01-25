from typing import ClassVar

from invest_iq.engines.utilities.logger.protocol import LoggerProtocol
from invest_iq.engines.utilities.validator.common.errors import ValidationError
from invest_iq.engines.utilities.validator.interface import ValidatorStrategy


class FieldValidator(ValidatorStrategy[dict]):
    """
    Extracts a field from a mapping and applies a sub-validator to it.

    Responsibilities
    ----------------
    - Enforce the presence of a specific field in a mapping.
    - Delegates validation of the field's value to a sub-validator.
    - Preserves error causality using exception chaining.
    """

    VALIDATOR_NAME : ClassVar[str]= "field"

    def __init__(
            self,
            logger: LoggerProtocol,
            field: str,
            validator: ValidatorStrategy,
    ):
        super().__init__(logger)
        self.field = field
        self.validator = validator

    def __call__(
            self,
            data: dict
    ):
        if not isinstance(data, dict):
            msg = f"[{self.VALIDATOR_NAME}] Expected dict, got {type(data).__name__}"
            raise ValidationError(msg)
        if self.field not in data:
            msg = f"[{self.VALIDATOR_NAME}] Missing field '{self.field}'"
            raise ValidationError(msg)
        try:
            self.validator(data[self.field])
        except ValidationError as e:
            msg = f"[{self.VALIDATOR_NAME}] Error in field '{self.field}': {e}"
            raise ValidationError(msg) from e