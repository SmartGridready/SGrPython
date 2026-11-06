"""
Tests the unit conversion (unitConversionMultiplicator) of REST data points
against a local HTTP server that plays the device.
"""

import os
from contextlib import asynccontextmanager
from typing import Any, Callable, Optional
from xml.sax.saxutils import escape

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from sgr_commhandler.device_builder import DeviceBuilder

EID_BASE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'eids'
)
SHELLY_1PM_EID = 'SGr_01_mmmm_dddd_Shelly_1PM_RestAPILocal_V0.1.xml'

# Functional profile list with the data points Power (read only) and Setpoint (read/write),
# both in kW with the device value in W. It replaces the functional profile list of the Shelly EID.
# The data type, the response query and the kind of read call (restApiReadServiceCall, or restApiServiceCall as
# in the older EIDs) of Power are parameters of the tests.
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
        <restApiDataPointConfiguration>
          <dataType>JSON_number</dataType>
          <@READ_CALL@>
            <requestMethod>GET</requestMethod>
            <requestPath>/status</requestPath>
            @RESPONSE_QUERY@
          </@READ_CALL@>
        </restApiDataPointConfiguration>
      </dataPointListElement>
      <dataPointListElement>
        <dataPoint>
          <dataPointName>Setpoint</dataPointName>
          <dataDirection>RW</dataDirection>
          <dataType><float64 /></dataType>
          <unit>KILOWATTS</unit>
          <unitConversionMultiplicator>0.001</unitConversionMultiplicator>
        </dataPoint>
        <restApiDataPointConfiguration>
          <dataType>JSON_number</dataType>
          <restApiReadServiceCall>
            <requestMethod>GET</requestMethod>
            <requestPath>/setpoint</requestPath>
            <responseQuery>
              <queryType>JMESPathExpression</queryType>
              <query>setpoint</query>
            </responseQuery>
          </restApiReadServiceCall>
          <restApiWriteServiceCall>
            <requestMethod>GET</requestMethod>
            <requestPath>/setpoint</requestPath>
            <requestQuery>
              <parameter>
                <name>value</name>
                <value>[[value]]</value>
              </parameter>
            </requestQuery>
          </restApiWriteServiceCall>
        </restApiDataPointConfiguration>
      </dataPointListElement>
    </dataPointList>
  </functionalProfileListElement>
</functionalProfileList>"""


def _shelly_eid() -> str:
    with open(os.path.join(EID_BASE_PATH, SHELLY_1PM_EID), encoding='utf-8') as eid_file:
        return eid_file.read()


def _eid(response_query: str = '', data_type: str = 'float64', read_call: str = 'restApiReadServiceCall') -> str:
    """
    Builds an EID from the Shelly EID, with the functional profiles of this test.
    """
    eid_xml = _shelly_eid()
    start = eid_xml.index('<functionalProfileList>')
    end = eid_xml.index('</functionalProfileList>') + len('</functionalProfileList>')
    functional_profiles = (
        _FUNCTIONAL_PROFILE_LIST
        .replace('@DATA_TYPE@', data_type)
        .replace('@RESPONSE_QUERY@', response_query)
        .replace('@READ_CALL@', read_call)
    )
    return eid_xml[:start] + functional_profiles + eid_xml[end:]


def _query(query_type: str, query: str) -> str:
    return (
        '<responseQuery>'
        f'<queryType>{query_type}</queryType><query>{escape(query)}</query>'
        '</responseQuery>'
    )


@asynccontextmanager
async def _fake_device(routes: dict[str, Callable[[web.Request], web.Response]]):
    """
    Starts a local HTTP server that plays the device, yields its base URI.
    """
    app = web.Application()
    for path, handler in routes.items():
        app.router.add_get(path, handler)
    server = TestServer(app)
    await server.start_server()
    try:
        yield f'http://{server.host}:{server.port}'
    finally:
        await server.close()


def _json_response(body: Any) -> Callable[[web.Request], Any]:
    async def handler(request: web.Request) -> web.Response:
        return web.json_response(body)
    return handler


def _text_response(body: str, content_type: str) -> Callable[[web.Request], Any]:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text=body, content_type=content_type)
    return handler


@asynccontextmanager
async def _connected_device(eid_xml: str, base_uri: str):
    device = DeviceBuilder().eid(eid_xml).properties(dict(base_uri=base_uri)).build()
    await device.connect_async()
    try:
        yield device
    finally:
        await device.disconnect_async()


async def _read(eid_xml: str, base_uri: str, data_point: tuple[str, str]) -> Any:
    async with _connected_device(eid_xml, base_uri) as device:
        return await device.get_data_point(data_point).get_value_async(skip_cache=True)


@pytest.mark.asyncio
async def test_rest_unit_conversion_shelly_eid():
    # Shelly 1PM: the device reports power in W and energy in Wmin, the data points are in kW and kWh
    routes = {
        '/status': _json_response({'meters': [{'power': 3000.0, 'total': 60000}]}),
        '/relay/0': _json_response({'ison': True}),
    }
    async with _fake_device(routes) as base_uri:
        eid_xml = _shelly_eid()
        power = await _read(eid_xml, base_uri, ('ActivePowerAC', 'ActivePowerACtot'))
        energy = await _read(eid_xml, base_uri, ('ActiveEnergyAC', 'ActiveEnergyACtot'))
        relay = await _read(eid_xml, base_uri, ('Relais', 'Relais'))

    assert power == pytest.approx(3.0)
    assert energy == pytest.approx(1.0)
    # no unitConversionMultiplicator, the value is passed on as is
    assert relay is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query_type, query, route',
    [
        ('JMESPathExpression', 'meters[0].power', _json_response({'meters': [{'power': 3000.0}]})),
        ('JMESPathExpression', 'power', _json_response({'power': 3000})),
        ('JMESPathExpression', 'power', _json_response({'power': '3000'})),
        ('JSONataExpression', 'meters[0].power', _json_response({'meters': [{'power': 3000.0}]})),
        ('RegularExpression', '[0-9.]+', _text_response('3000.0', 'text/plain')),
        ('XPathExpression', '//power/text()', _text_response('<status><power>3000.0</power></status>', 'application/xml')),
    ],
)
async def test_rest_unit_conversion_response_query(query_type: str, query: str, route: Callable[[web.Request], Any]):
    async with _fake_device({'/status': route}) as base_uri:
        value = await _read(_eid(_query(query_type, query)), base_uri, ('Test', 'Power'))

    assert value == pytest.approx(3.0)


@pytest.mark.asyncio
async def test_rest_unit_conversion_service_call_of_older_eids():
    # many EIDs use the single restApiServiceCall instead of restApiReadServiceCall
    eid_xml = _eid(_query('JMESPathExpression', 'power'), read_call='restApiServiceCall')
    async with _fake_device({'/status': _json_response({'power': 3000.0})}) as base_uri:
        value = await _read(eid_xml, base_uri, ('Test', 'Power'))

    assert value == pytest.approx(3.0)


@pytest.mark.asyncio
async def test_rest_unit_conversion_plain_response():
    async with _fake_device({'/status': _text_response('3000.0', 'text/plain')}) as base_uri:
        value = await _read(_eid(), base_uri, ('Test', 'Power'))

    assert value == pytest.approx(3.0)


@pytest.mark.asyncio
async def test_rest_unit_conversion_not_applied_to_structures():
    # the result of the response query is not a number, there is nothing to convert
    status = {'meters': [{'power': 3000.0}]}
    mapping = (
        '<responseQuery><queryType>JMESPathMapping</queryType><jmesPathMappings>'
        '<mapping><from>meters[*].power</from><to>[*].power</to></mapping>'
        '</jmesPathMappings></responseQuery>'
    )
    async with _fake_device({'/status': _json_response(status)}) as base_uri:
        queried = await _read(_eid(_query('JMESPathExpression', 'meters'), 'json'), base_uri, ('Test', 'Power'))
        mapped = await _read(_eid(mapping, 'json'), base_uri, ('Test', 'Power'))

    assert queried == status['meters']
    # a mapping only restructures the JSON, its values are not converted
    assert mapped == [{'power': 3000.0}]


@pytest.mark.asyncio
async def test_rest_unit_conversion_write_and_read_back():
    device_state: dict[str, Optional[str]] = {'setpoint': None}
    received: list[str] = []

    async def setpoint(request: web.Request) -> web.Response:
        if 'value' in request.query:
            received.append(request.query['value'])
            device_state['setpoint'] = request.query['value']
        return web.json_response({'setpoint': float(device_state['setpoint'] or 0)})

    async with _fake_device({'/setpoint': setpoint}) as base_uri:
        async with _connected_device(_eid(), base_uri) as device:
            data_point = device.get_data_point(('Test', 'Setpoint'))
            await data_point.set_value_async(3.0)
            value = await data_point.get_value_async(skip_cache=True)

    # the device gets W, the data point is in kW
    assert [float(v) for v in received] == [3000.0]
    assert value == pytest.approx(3.0)
