from sgrspecification.product import ConfigurationListElement, ConfigurationList


def build_configurations_parameters(params: ConfigurationList):
    if params is None:
        return []
    return [ConfigurationParameter(x) for x in params.configuration_list_element]


class ConfigurationParameter:

    def __init__(self, parameter: ConfigurationListElement):
        translation = parameter.configuration_description
        self.label = translation[0].label
        self.match = parameter.name
        self.type = parameter.data_type
        self.description = translation[0].text_element

    def __str__(self):
        return f'{self.label} - {self.match}'

    def __repr__(self):
        return f'{self.label} - {self.match}'
