import logging
from sgr_specification.v0.generic.base_types import (
    JmesPathMappingRecord
)

logger = logging.getLogger(__name__)


def map_json_response(response: str, mappings: list[JmesPathMappingRecord]) -> str:
    if len(mappings) == 0:
        return response
    return ""
