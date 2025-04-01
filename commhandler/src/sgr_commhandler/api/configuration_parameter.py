from typing import Optional

from sgr_specification.v0.product import (
    ConfigurationList,
    ConfigurationListElement,
)


def build_configuration_parameters(params: Optional[ConfigurationList]) -> list['ConfigurationParameter']:
    """
    Constructs a configuration parameter list.

    Parameters
    ----------
    params : Optional[ConfigurationList]
        The configuration list of an EID
    
    Returns
    -------
    list[ConfigurationParameter]
        a list of configuration parameters
    """

    if params is None:
        return []
    return [
        ConfigurationParameter(x) for x in params.configuration_list_element
    ]


class ConfigurationParameter:
    """
    Implements an EID configuration parameter.
    """

    def __init__(self, parameter: ConfigurationListElement):
        """
        Constructs a configuration parameter.

        Parameters
        ----------
        parameter : ConfigurationListElement
            A configuration list element of the SGr specification
        """
        
        translation = parameter.configuration_description
        self.label = translation[0].label
        self.name = parameter.name
        self.type = parameter.data_type
        self.description = translation[0].text_element
        self.default_value = parameter.default_value

    def __str__(self) -> str:
        """
        Converts to string.

        Returns
        ----------
        str
            A string
        """

        return f'{self.label} - {self.name}'

    def __repr__(self):
        """
        Gets an object description as string.

        Returns
        ----------
        str
            A string
        """

        return f'{self.label} - {self.name}'
