import json

from sgr_specification.v0.generic.base_types import (
    JmespathMappingRecord
)
from sgr_commhandler.utils import (
    jmespath_mapping
)

"""
Test JMESPath mapping.
"""

def test_jmespath_mapping():
    jmes_mappings = [
        JmespathMappingRecord(from_value="[*].start_timestamp", to="[*].start_timestamp"),
        JmespathMappingRecord(from_value="[*].end_timestamp", to="[*].end_timestamp"),
        JmespathMappingRecord(from_value="[*].vario_grid", to="[*].integrated[*].value"),
        JmespathMappingRecord(from_value="[*].unit", to="[*].integrated[*].unit")
    ]
    json_input = json.dumps([
        {
            "start_timestamp": "2023-09-06T00:00:00+02:00",
            "end_timestamp": "2023-09-06T00:15:00+02:00",
            "vario_plus": 32.09,
            "vario_grid": 9.23,
            "dt_plus": 25.08,
            "unit": "Rp./kWh"
        },
        {
            "start_timestamp": "2023-09-06T00:15:00+02:00",
            "end_timestamp": "2023-09-06T00:30:00+02:00",
            "vario_plus": 31.25,
            "vario_grid": 8.46,
            "dt_plus": 25.08,
            "unit": "Rp./kWh"
        }
    ])
    json_expected = json.dumps([
        {
            "start_timestamp": "2023-09-06T00:00:00+02:00",
            "end_timestamp": "2023-09-06T00:15:00+02:00",
            "integrated": [
                {
                    "value": 9.23,
                    "unit": "Rp./kWh"
                }
            ]
        },
        {
            "start_timestamp": "2023-09-06T00:15:00+02:00",
            "end_timestamp": "2023-09-06T00:30:00+02:00",
            "integrated": [
                {
                    "value": 8.46,
                    "unit": "Rp./kWh"
                }
            ]
        }
    ])

    json_mapped = jmespath_mapping.map_json_response(json_input, jmes_mappings)
    assert json_mapped is json_expected
