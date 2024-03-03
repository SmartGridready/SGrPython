from sgr_library.generated.product import ConfigurationListElement, ConfigurationList


def build_configurations_parameters(params: ConfigurationList):
    return [ConfigurationParameter(x) for x in params.configuration_list_element]


class ConfigurationParameter:

    def __init__(self, parameter: ConfigurationListElement):
        translation = parameter.configuration_description
        self.label = translation[0].label
        self.match = parameter.name
        self.type = parameter.data_type
        self.description = translation[0].text_element
