import logging
from sgr_specification.v0.generic.base_types import (
    JmespathMappingRecord
)

logger = logging.getLogger(__name__)


def map_json_response(response: str, mappings: list[JmespathMappingRecord]) -> str:
    if len(mappings) == 0:
        return response
    return ""
