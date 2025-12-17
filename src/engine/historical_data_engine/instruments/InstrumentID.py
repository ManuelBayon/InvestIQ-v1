from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class InstrumentID:

    code : str

    @classmethod
    def from_symbol(cls, raw_symbol: str) -> "InstrumentID":
        cleaned_symbol = raw_symbol.replace('/', '').replace('-', '').replace('_', '')
        return cls(code=cleaned_symbol)

    @classmethod
    def from_enum(cls, enum_value: Enum) -> "InstrumentID":
        return cls(code=enum_value.value)

    def __str__(self) -> str:
        return self.code

    def __eq__(self, other:object) -> bool:
        if isinstance(other, InstrumentID):
            return self.code == other.code
        elif isinstance(other, str):
            return self.code == InstrumentID.from_symbol(other).code
        return False

    def __hash__(self) -> int:
        return hash(self.code)