"""
Provides dynamic request parameters.
"""

import logging
from typing import Optional

from sgr_specification.v0.generic.base_types import (
    DynamicParameterDescriptionList,
    DynamicParameterDescriptionListElement
)

logger = logging.getLogger(__name__)


def build_dynamic_parameters(params: Optional[DynamicParameterDescriptionList]) -> list['DynamicParameter']:
    """
    Constructs a dynamic parameter list.

    Parameters
    ----------
    params : Optional[DynamicParameterDescriptionList]
        The dynamic parameter list of a data point

    Returns
    -------
    list[DynamicParameter]
        a list of dynamic parameters
    """
    if params is None:
        return []
    return [
        DynamicParameter(x) for x in params.parameter_list_element
    ]


def build_dynamic_parameter_substitutions(dynamic_parameters: list['DynamicParameter'], input_parameters: Optional[dict[str, str]]) -> dict[str, str]:
    """
    Builds dynamic parameter substitutions, to be used in data point requests.
    Only parameters defined in the dynamic parameter list are kept.
    Parameters not defined in the properties are set to the default value.

    Parameters
    ----------
    dynamic_parameters: list[DynamicParameter]
        the dynamic parameters as specified
    input_parameters: Optional[dict[str, str]]
        the actual parameters given to the request

    Returns
    -------
    Dict[str, str]
        the final substitutions as dictionary
    """
    final_parameters = {}
    for dyn_param in dynamic_parameters:
        prop_value = input_parameters.get(str(dyn_param.name)) if input_parameters is not None else None
        if prop_value is not None:
            final_parameters[dyn_param.name] = prop_value
        elif dyn_param.default_value is not None:
            final_parameters[dyn_param.name] = dyn_param.default_value
        logger.debug(f'dynamic parameter: {dyn_param.name} = {final_parameters[dyn_param.name]}')
    return final_parameters


class DynamicParameter:
    """
    Implements a dynamic parameter of data points.
    """

    def __init__(self, parameter: DynamicParameterDescriptionListElement):
        """
        Constructs a dynamic parameter.

        Parameters
        ----------
        parameter : DynamicParameterDescriptionListElement
            A dynamic parameter list element of the SGr specification
        """
        translation = parameter.parameter_description
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
        return f'<DynamicParameter={self.name}>'
