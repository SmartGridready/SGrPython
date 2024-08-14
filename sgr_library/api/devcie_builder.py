from enum import Enum

class SGrConfiguration(Enum):
    UNKNOWN = 1
    STRING = 2
    FILE = 3


class SGrDeviceProtocol(Enum):
    MODBUS_RTU = 0
    MODBUS_TPC = 1
    RESTAPI = 2
    GENERIC = 3
    CONTACT = 4

class DeviceBuilder:

    def __init__(self):
        self._value: str | None = None
        self._config_value: str | dict | None = None
        self._type: SGrConfiguration = SGrConfiguration.UNKNOWN
        self._config_type: SGrConfiguration = SGrConfiguration.UNKNOWN


    def build(self) -> SgrRestInterface | SgrModbusInterface | SgrModbusRtuInterface:
        if self._type not in loaders:
            raise Exception(f'unsupported loader configuration, {self._type}')

        spec, config = self.replace_variables()
        xml = loaders[SGrConfiguration.STRING](spec)
        protocol = resolve_protocol(xml)
        return device_builders[protocol](xml, config)
