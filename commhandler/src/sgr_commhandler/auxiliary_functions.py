from pymodbus.constants import Endian
from sgr_specification.v0.product import BitOrder


def get_address(root) -> str:
    try:
        return str(
            root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.address
        )
    except AttributeError:
        raise ValueError("IP address not found in XML file.")


def get_port(root) -> int:
    try:
        return int(
            root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.port
        )
    except (AttributeError, ValueError):
        raise ValueError("Port not found or invalid in XML file.")


def get_slave(root) -> int:
    try:
        return int(
            root.interface_list.modbus_interface.modbus_interface_description.modbus_tcp.slave_id
        )
    except (AttributeError, ValueError):
        raise ValueError("Slave ID not found or invalid in XML file.")


def get_slave_rtu(root) -> int:
    try:
        return int(
            root.interface_list.modbus_interface.modbus_interface_description.modbus_rtu.slave_addr
        )
    except (AttributeError, ValueError):
        raise ValueError("RTU Slave ID not found or invalid in XML file.")


def get_endian(root) -> Endian:
    try:
        match root.interface_list.modbus_interface.modbus_interface_description.bit_order:
            case BitOrder.BIG_ENDIAN:
                return Endian.BIG
            case _:
                return Endian.LITTLE
    except AttributeError:
        raise ValueError("Endian type not found in XML file.")
