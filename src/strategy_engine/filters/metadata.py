from dataclasses import dataclass


@dataclass(frozen=True)
class FilterMetadata:
    filter_uuid: str
    created_at: str
    name: str
    version: str
    description: str
    parameters: dict[str, object]
    required_fields : list[str]
    produced_features: list[str]
    diagnostics_schema: list[str]