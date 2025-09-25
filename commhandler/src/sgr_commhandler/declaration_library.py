from typing import Any
import requests

LIB_BASE_URL = 'https://library.smartgridready.ch'

def get_product_eid_xml(name: str) -> str:
    """
    Gets the XML data of a product EID.

    Parameters
    ----------
    name : str
        the EID name

    Returns
    -------
    str
        an XML string
    """
    headers = {'Accept': 'application/xml;charset=UTF-8'}
    response = requests.get(f'{LIB_BASE_URL}/prodx/{name}', headers=headers)
    if response.status_code == 200:
        return response.text
    raise Exception(f'request failed with status={response.status_code}')


def get_product_info(name: str) -> Any:
    """
    Gets information about a product EID.

    Parameters
    ----------
    name : str
        the EID name

    Returns
    -------
    str
        a JSON object
    """
    headers = {'Accept': 'application/json;charset=UTF-8'}
    response = requests.get(f'{LIB_BASE_URL}/prods/{name}', headers=headers)
    if response.status_code == 200:
        return response.json()
    raise Exception(f'request failed with status={response.status_code}')
