from sgr_library.generated.product import ConfigurationListElement, ConfigurationList


def build_configurations_parameters(params: ConfigurationList):
    return [ConfigurationParameter(x) for x in params.configuration_list_element]


class ConfigurationParameter:

    def __init__(self, parameter: ConfigurationListElement):
        self.label = parameter.name
        self.match = parameter.name
        self.type = parameter.data_type
        self.description = parameter.legible_description
        x = self.description[0].text_element
