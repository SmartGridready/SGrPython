import re

from sgr_library.api import BaseSGrInterface, FunctionProfile, DeviceInformation
from sgr_library.generic_interface import GenericSGrDeviceBuilder


class SGrDevice(BaseSGrInterface):

    def __init__(self):
        self._builder: GenericSGrDeviceBuilder = GenericSGrDeviceBuilder()
        self._interface: BaseSGrInterface | None = None
        self._configuration_params: list[str] = []

    def get_configuration_params(self) -> set[str]:
        return {param for param in self._configuration_params}

    def is_connect(self):
        return self._interface is not None

    async def connect(self):
        self._interface = self._builder.build()
        await self._interface.connect()

    def update_config(self, config: dict | str) -> 'SGrDevice':
        if isinstance(config, str):
            self._builder.config_file_path(config)
        else:
            self._builder.config(config)

        return self

    def show_replacement(self):
        content, _ = self._builder.replace_variables()
        return content

    def update_xml_spec(self, spec: str) -> 'SGrDevice':
        content = spec
        if spec.startswith("<?xml"):
            self._builder.xml_string(spec)
        else:
            self._builder.xml_file_path(spec)
            content = self._builder.get_spec_content()
        pattern = r'{{[a-zA-Z0-9_]*}}'
        found_params: list[str] = re.findall(pattern, content)
        self._configuration_params = [found_param.removesuffix('}}').removeprefix('{{') for found_param in found_params]
        return self

    def get_function_profiles(self) -> dict[str, FunctionProfile]:
        return self._interface.get_function_profiles()

    def build(self):
        self._interface = self._builder.build()

    def device_information(self) -> DeviceInformation:
        return self._interface.device_information()
