from enum import Enum

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class LevelOfOperation(Enum):
    """
    maturity level concerning SmartGridread functionality.

    :cvar M: m: monitoring only
    :cvar VALUE_1: 1: binary writable data points
    :cvar VALUE_2: 2: discrete writable data points
    :cvar VALUE_3: 3: fixed set of characteristic curves
    :cvar VALUE_4: 4: dynamic set values
    :cvar VALUE_5: 5: dynamic characteristic curves
    :cvar VALUE_6: 6: predictive
    :cvar VALUE_1M: 1m: binary writable data points plus monitoring
    :cvar VALUE_2M: 2m: discrete writable data points plus monitoring
    :cvar VALUE_3M: 3m: fixed set of characteristic curves plus
        monitoring
    :cvar VALUE_4M: 4m: dynamic set values plus monitoring
    :cvar VALUE_5M: 5m: dynamic characteristic curves plus monitoring
    :cvar VALUE_6M: 6m: predictive plus monitoring
    """
    M = "m"
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_6 = "6"
    VALUE_1M = "1m"
    VALUE_2M = "2m"
    VALUE_3M = "3m"
    VALUE_4M = "4m"
    VALUE_5M = "5m"
    VALUE_6M = "6m"
