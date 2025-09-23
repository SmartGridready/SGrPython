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

def test_jmespath_mapping_1():
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
    assert json_mapped == json_expected


def test_jmespath_mapping_2():
    jmes_mappings = [
        JmespathMappingRecord(from_value="prices[*].start_timestamp", to="[*].start_timestamp"),
        JmespathMappingRecord(from_value="prices[*].end_timestamp", to="[*].end_timestamp"),
        #JmespathMappingRecord(from_value="prices[*].integrated[*].value", to="[*].integrated[*].value"),
        #JmespathMappingRecord(from_value="prices[*].integrated[*].unit", to="[*].integrated[*].unit"),
        #JmespathMappingRecord(from_value="prices[*].integrated[*].component", to="[*].integrated[*].component")
        JmespathMappingRecord(from_value="prices[*].*[*].value", to="[*].*[*].value"),
        JmespathMappingRecord(from_value="prices[*].*[*].unit", to="[*].*[*].unit"),
        JmespathMappingRecord(from_value="prices[*].*[*].component", to="[*].*[*].component")
    ]
    json_input = json.dumps({
        "status": "ok",
        "prices": [
            {
                "start_timestamp": "2025-01-01T00:00:00+01:00",
                "end_timestamp": "2025-01-01T00:15:00+01:00",
                "integrated": [
                    {
                        "value": 4.7,
                        "unit": "CHF/kWh",
                        "component": "work"
                    }
                ],
                "grid": [
                    {
                        "value": 1.7,
                        "unit": "CHF/kWh",
                        "component": "work"
                    }
                ]
            },
            {
                "start_timestamp": "2025-01-01T00:15:00+01:00",
                "end_timestamp": "2025-01-01T00:30:00+01:00",
                "integrated": [
                    {
                        "value": 4.698633,
                        "unit": "CHF/kWh",
                        "component": "work"
                    }
                ],
                "grid": [
                    {
                        "value": 2.7,
                        "unit": "CHF/kWh",
                        "component": "work"
                    }
                ]
            }
        ]
    })
    json_expected = json.dumps([
        {
            "start_timestamp": "2025-01-01T00:00:00+01:00",
            "end_timestamp": "2025-01-01T00:15:00+01:00",
            "integrated": [
                {
                    "value": 4.7,
                    "unit": "CHF/kWh",
                    "component": "work"
                }
            ]
        },
        {
            "start_timestamp": "2025-01-01T00:15:00+01:00",
            "end_timestamp": "2025-01-01T00:30:00+01:00",
            "integrated": [
                {
                    "value": 4.698633,
                    "unit": "CHF/kWh",
                    "component": "work"
                }
            ]
        }
    ])

    json_mapped = jmespath_mapping.map_json_response(json_input, jmes_mappings)
    assert json_mapped == json_expected

