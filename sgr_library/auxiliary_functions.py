from pymodbus.constants import Endian

from sgr_library.data_classes.product import DeviceFrame

from exceptions import DataPointException, FunctionalProfileException, InvalidEndianType

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser


# TODO error handling
def get_protocol(xml_file:str) -> str:
    """
    Searches for protocol type in xml file
    :return: protocol type string
    """
    parser = XmlParser(context=XmlContext())
    root = parser.parse(xml_file, DeviceFrame)

    restapi = root.interface_list.rest_api_interface
    generic = root.interface_list.generic_interface
    contact = root.interface_list.contact_interface
    modbus = root.interface_list.modbus_interface
    if modbus:
        return "modbus"
    elif restapi:
        return "restapi"
    elif generic:
        return "generic"
    elif contact:
        return "contact"
    else:
        return "error"

# TODO make this one so that it is generic.
def find_dp(root, fp_name: str, dp_name: str):
    """
    Searches the datapoint in the root element.
    :param root: The root element created with the xsdata parser
    :param fp_name: The name of the funcitonal profile in which the datapoint resides
    :param dp_name: The name of the datapoint
    :returns: The datapoint element found in root, if not, returns None.
    """

    fp = next(filter(lambda x: x.functional_profile.functional_profile_name == fp_name, root.interface_list.modbus_interface.functional_profile_list.functional_profile_list_element), None)
    if fp:
        dp = next(filter(lambda x: x.data_point.data_point_name == dp_name, fp.data_point_list.data_point_list_element), None)
        if dp:
            print(dp)
        raise DataPointException(f"Datapoint {dp_name} not found in functional profile {fp_name}.")
    raise FunctionalProfileException(f"Functional profile {fp_name} not found in XML file.")

def get_modbusInterfaceSelection(xml_file: str) -> str:
    try:
        parser = XmlParser(context=XmlContext())
        root = parser.parse(xml_file, DeviceFrame)
        interface_selection = root.interface_list.modbus_interface.modbus_interface_description.modbus_interface_selection.value
        if interface_selection not in ['RTU', 'TCP/IP', 'UDP/IP', 'RTU-ASCII', 'TCP/IP-ASCII', 'UDP/IP-ASCII']:
            raise ValueError('Invalid Modbus interface selection found.')
        return interface_selection
    except Exception as e:
        raise ValueError(f"Error parsing XML file or extracting Modbus interface selection: {e}")

def get_address(root) -> str:
    try:
        return str(root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.address)
    except AttributeError:
        raise ValueError("IP address not found in XML file.")

def get_port(root) -> int:
    try:
        return int(root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.port)
    except (AttributeError, ValueError):
        raise ValueError("Port not found or invalid in XML file.")

def get_slave(root) -> int:
    try:
        return int(root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.slave_id)
    except (AttributeError, ValueError):
        raise ValueError("Slave ID not found or invalid in XML file.")

def get_slave_rtu(root) -> int:
    try:
        return int(root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.slave_addr)
    except (AttributeError, ValueError):
        raise ValueError("RTU Slave ID not found or invalid in XML file.")

def get_endian(root) -> str:
    try:
        endian_str = str(root.interface_list.modbus_interface.modbus_interface_description.bit_order.value)
        if endian_str == "BigEndian":
            return Endian.Big
        elif endian_str == "LittleEndian":
            return Endian.Little
        else:
            raise InvalidEndianType(f'received invalid endian type: "{endian_str}"')
    except AttributeError:
        raise ValueError("Endian type not found in XML file.")

def get_baudrate(root) -> int:
    try:
        return int(root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.baud_rate_selected.value)
    except (AttributeError, ValueError):
        raise ValueError("Baudrate not found or invalid in XML file.")

def get_parity(root) -> str:
    try:
        parity_string = str(root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.parity_selected.value)
        if parity_string == "EVEN":
            return "E"
        else:
            raise NotImplementedError(f'Parity type "{parity_string}" not supported.')
    except AttributeError:
        raise ValueError("Parity type not found in XML file.")
    