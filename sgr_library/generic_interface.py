from sgr_library.modbus_interface import SgrModbusInterface
from sgr_library.restapi_client_async import SgrRestInterface
import os

import asyncio
from sgr_library.auxiliary_functions import get_protocol, get_modbusInterfaceSelection, xml_variable_substitution
from sgr_library.modbusRTU_interface_async import SgrModbusRtuInterface


class GenericInterface:

    def __new__(cls, xml_file: str, config_file=None):
        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"The specified XML file does not exist: {xml_file}")

        try:
            protocol_type = get_protocol(xml_file)
        except Exception as e:
            raise Exception(f"Error in getting protocol from XML: {e}")

        if protocol_type == "modbus":
            try:
                modbus_protocol_type = get_modbusInterfaceSelection(xml_file)
            except Exception as e:
                raise Exception(f"Error in getting Modbus interface selection: {e}")

            if modbus_protocol_type == "TCPIP":
                obj = object.__new__(SgrModbusInterface)
                obj.__init__(xml_file)
            elif modbus_protocol_type == "RTU":
                obj = object.__new__(SgrModbusRtuInterface)
                obj.__init__(xml_file)
            else:
                raise ValueError(f"Unsupported Modbus protocol type: {modbus_protocol_type}")
            return obj
            
        elif protocol_type == "restapi":
            obj = object.__new__(SgrRestInterface)
            obj.__init__(xml_variable_substitution(xml_file, config_file))
            return obj
            
        else:
            raise ValueError(f"Unsupported protocol type: {protocol_type}")
