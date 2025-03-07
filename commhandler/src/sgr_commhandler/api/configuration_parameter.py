from typing import Optional

from sgr_specification.v0.product import (
    ConfigurationList,
    ConfigurationListElement,
)


def build_configurations_parameters(params: Optional[ConfigurationList]):
    if params is None:
        return []
    return [
        ConfigurationParameter(x) for x in params.configuration_list_element
    ]


class ConfigurationParameter:
    def __init__(self, parameter: ConfigurationListElement):
        translation = parameter.configuration_description
        self.label = translation[0].label
        self.name = parameter.name
        self.type = parameter.data_type
        self.description = translation[0].text_element
        self.default_value = parameter.default_value

    def __str__(self):
        return f'{self.label} - {self.name}'

    def __repr__(self):
        return f'{self.label} - {self.name}'
