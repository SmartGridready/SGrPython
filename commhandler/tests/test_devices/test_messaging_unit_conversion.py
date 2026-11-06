"""
Tests the unit conversion (unitConversionMultiplicator) of messaging data points.

The messages are delivered to the device like the MQTT client does it, there is no broker.
"""

import json
import os
from typing import Any

import pytest

from sgr_commhandler.device_builder import DeviceBuilder

EID_BASE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'eids'
)
MQTT_EID = 'SGr_XX_HiveMQ_MQTT_Cloud.xml'
MQTT_PROPERTIES = dict(host='localhost', port='1883', username='test', password='test')

STATUS_TOPIC = 'shellies/test/status/switch:0'
ENERGY_TOPIC = 'shellies/test/status/energy'
SETPOINT_TOPIC = 'test/setpoint'
SETPOINT_CMD_TOPIC = 'test/setpoint/set'

# Functional profile list with the data points Power and Energy (read only), Setpoint (read/write),
# all with a device value in W or Wh and a data point in kW or kWh. It replaces the functional profile list
# of the MQTT test EID. The data type, the message data type and the response query of Power are parameters of the tests,
# so is the topic of Energy (the payloads of the tests are not all JSON, a message must not reach Energy by accident).
_FUNCTIONAL_PROFILE_LIST = """<functionalProfileList>
  <functionalProfileListElement>
    <functionalProfile>
      <functionalProfileName>Test</functionalProfileName>
      <functionalProfileIdentification>
        <specificationOwnerIdentification>0</specificationOwnerIdentification>
        <functionalProfileCategory>Metering</functionalProfileCategory>
        <functionalProfileType>ActivePowerAC</functionalProfileType>
        <levelOfOperation>m</levelOfOperation>
        <versionNumber>
          <primaryVersionNumber>1</primaryVersionNumber>
          <secondaryVersionNumber>1</secondaryVersionNumber>
          <subReleaseVersionNumber>0</subReleaseVersionNumber>
        </versionNumber>
      </functionalProfileIdentification>
    </functionalProfile>
    <dataPointList>
      <dataPointListElement>
        <dataPoint>
          <dataPointName>Power</dataPointName>
          <dataDirection>R</dataDirection>
          <dataType><@DATA_TYPE@ /></dataType>
          <unit>KILOWATTS</unit>
          <unitConversionMultiplicator>0.001</unitConversionMultiplicator>
        </dataPoint>
        <messagingDataPointConfiguration>
          <messagingDataType><@MESSAGING_TYPE@ /></messagingDataType>
          <inMessage>
            <topic>@STATUS_TOPIC@</topic>
            @RESPONSE_QUERY@
          </inMessage>
        </messagingDataPointConfiguration>
      </dataPointListElement>
      <dataPointListElement>
        <dataPoint>
          <dataPointName>Energy</dataPointName>
          <dataDirection>R</dataDirection>
          <dataType><float64 /></dataType>
          <unit>KILOWATT_HOURS</unit>
          <unitConversionMultiplicator>0.001</unitConversionMultiplicator>
        </dataPoint>
        <messagingDataPointConfiguration>
          <messagingDataType><number /></messagingDataType>
          <inMessage>
            <topic>@ENERGY_TOPIC@</topic>
            <responseQuery>
              <queryType>JMESPathExpression</queryType>
              <query>aenergy.total</query>
            </responseQuery>
          </inMessage>
        </messagingDataPointConfiguration>
      </dataPointListElement>
      <dataPointListElement>
        <dataPoint>
          <dataPointName>Setpoint</dataPointName>
          <dataDirection>RW</dataDirection>
          <dataType><float64 /></dataType>
          <unit>KILOWATTS</unit>
          <unitConversionMultiplicator>0.001</unitConversionMultiplicator>
        </dataPoint>
        <messagingDataPointConfiguration>
          <messagingDataType><number /></messagingDataType>
          <writeCmdMessage>
            <topic>@SETPOINT_CMD_TOPIC@</topic>
            <template>[[value]]</template>
          </writeCmdMessage>
          <inMessage>
            <topic>@SETPOINT_TOPIC@</topic>
            <responseQuery>
              <queryType>JMESPathExpression</queryType>
              <query>setpoint</query>
            </responseQuery>
          </inMessage>
        </messagingDataPointConfiguration>
      </dataPointListElement>
    </dataPointList>
  </functionalProfileListElement>
</functionalProfileList>"""


def _eid(
    response_query: str = '', data_type: str = 'float64', messaging_type: str = 'number', energy_topic: str = ENERGY_TOPIC
) -> str:
    """
    Builds an EID from the MQTT test EID, with the functional profiles of this test.
    """
    with open(os.path.join(EID_BASE_PATH, MQTT_EID), encoding='utf-8') as eid_file:
        eid_xml = eid_file.read()
    start = eid_xml.index('<functionalProfileList>')
    end = eid_xml.index('</functionalProfileList>') + len('</functionalProfileList>')
    functional_profiles = (
        _FUNCTIONAL_PROFILE_LIST
        .replace('@DATA_TYPE@', data_type)
        .replace('@MESSAGING_TYPE@', messaging_type)
        .replace('@RESPONSE_QUERY@', response_query)
        .replace('@STATUS_TOPIC@', STATUS_TOPIC)
        .replace('@ENERGY_TOPIC@', energy_topic)
        .replace('@SETPOINT_TOPIC@', SETPOINT_TOPIC)
        .replace('@SETPOINT_CMD_TOPIC@', SETPOINT_CMD_TOPIC)
    )
    return eid_xml[:start] + functional_profiles + eid_xml[end:]


def _query(query_type: str, query: str) -> str:
    return (
        '<responseQuery>'
        f'<queryType>{query_type}</queryType><query>{query}</query>'
        '</responseQuery>'
    )


def _device(eid_xml: str):
    return DeviceBuilder().eid(eid_xml).properties(MQTT_PROPERTIES).build()


async def _receive(eid_xml: str, payload: Any, data_point: str = 'Power') -> Any:
    """
    Delivers a message to the device and reads the value of the data point.
    """
    device = _device(eid_xml)
    device.handle_client_message(STATUS_TOPIC, payload)
    return await device.get_data_point(('Test', data_point)).get_value_async()


@pytest.mark.asyncio
async def test_messaging_unit_conversion_shelly_status():
    # status message of a Shelly Pro4PM, the MQTT client delivers the payload as bytes
    payload = json.dumps({
        'id': 0, 'source': 'init', 'output': True,
        'apower': 3000.0, 'voltage': 230.0, 'current': 13.0,
        'aenergy': {'total': 1500.0, 'by_minute': [0.0, 0.0, 0.0], 'minute_ts': 1730000000},
    }).encode('utf-8')
    eid_xml = _eid(_query('JMESPathExpression', 'apower'), energy_topic=STATUS_TOPIC)
    device = _device(eid_xml)

    device.handle_client_message(STATUS_TOPIC, payload)

    # power in W is read as kW, energy in Wh as kWh
    assert await device.get_data_point(('Test', 'Power')).get_value_async() == pytest.approx(3.0)
    assert await device.get_data_point(('Test', 'Energy')).get_value_async() == pytest.approx(1.5)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_type, query, payload',
    [
        ('JMESPathExpression', 'apower', '{"apower": 3000.0}'),
        ('JMESPathExpression', 'apower', '{"apower": 3000}'),
        ('JMESPathExpression', 'apower', '{"apower": "3000"}'),
        ('JSONataExpression', 'apower', '{"apower": 3000.0}'),
        ('RegularExpression', '[0-9.]+', '3000.0'),
        ('XPathExpression', '//apower/text()', '<status><apower>3000.0</apower></status>'),
    ],
)
async def test_messaging_unit_conversion_response_query(query_type: str, query: str, payload: str):
    value = await _receive(_eid(_query(query_type, query)), payload)

    assert value == pytest.approx(3.0)


@pytest.mark.asyncio
async def test_messaging_unit_conversion_plain_message():
    value = await _receive(_eid(), '3000.0')

    assert value == pytest.approx(3.0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'response_query, data_type, messaging_type, payload, expected',
    [
        # a JSON object is not converted
        (_query('JMESPathExpression', 'meters'), 'json', 'JSON_array', '{"meters": [{"apower": 3000.0}]}', [{'apower': 3000.0}]),
        # nor is a text
        (_query('JMESPathExpression', 'label'), 'string', 'number', '{"label": "n/a"}', 'n/a'),
        # a JMESPath mapping only restructures the JSON, its values are not converted
        (
            '<responseQuery><queryType>JMESPathMapping</queryType><jmesPathMappings>'
            '<mapping><from>meters[*].apower</from><to>[*].power</to></mapping>'
            '</jmesPathMappings></responseQuery>',
            'json', 'JSON_array', '{"meters": [{"apower": 3000.0}]}', [{'power': 3000.0}],
        ),
    ],
)
async def test_messaging_unit_conversion_not_applied_to_structures(
    response_query: str, data_type: str, messaging_type: str, payload: str, expected: Any
):
    value = await _receive(_eid(response_query, data_type, messaging_type), payload)

    assert value == expected


@pytest.mark.asyncio
async def test_messaging_unit_conversion_write_and_read_back(monkeypatch: pytest.MonkeyPatch):
    device = _device(_eid())
    sent: list[tuple[str, Any]] = []

    async def write_message(topic: str, payload: Any):
        sent.append((topic, payload))

    monkeypatch.setattr(device, 'write_message', write_message)
    data_point = device.get_data_point(('Test', 'Setpoint'))

    await data_point.set_value_async(3.0)

    # the device gets W, the data point is in kW
    assert [(topic, float(payload)) for topic, payload in sent] == [(SETPOINT_CMD_TOPIC, 3000.0)]

    # the device confirms the new setpoint on its status topic, in W
    device.handle_client_message(SETPOINT_TOPIC, json.dumps({'setpoint': float(sent[0][1])}).encode('utf-8'))
    assert await data_point.get_value_async() == pytest.approx(3.0)
