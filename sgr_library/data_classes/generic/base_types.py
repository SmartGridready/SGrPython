from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate
from data_classes.generic.base_type_functional_profile_category import FunctionalProfileCategory
from data_classes.generic.base_type_functional_profile_type import FunctionalProfileType
from data_classes.generic.base_type_level_of_operation_type import LevelOfOperation

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class AlternativeNames:
    """a name list for EEBUS, IEC6850,, SAREF4ENER etc.

    Used to support onology naming.

    :ivar work_name: work name for temporary use
    :ivar manuf_name: manufacturers may use an internal wording
    :ivar iec61850_name: IEC 61850 termonoligy place to add the 61850
        abreviatuions
    :ivar saref_name: SAREF for ENER termonoligy place to add the SAREF
        abreviations (https://saref.etsi.org)
    :ivar eebus_name: EEBUS for terminology place to add the EEBUS
        abreviations
    :ivar sun_spec_name: sSUNSPEC for terminology place to add the
        www.sunspec.org abreviations
    :ivar hp_bwp_name: bwp (German Heat Pump Association) for
        terminology place to add the bwp naming for HVAC
    :ivar en17609_name: EN17609 terminology place to add the EU17609
        abbreviations
    """
    work_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "workName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    manuf_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "manufName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    iec61850_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "iec61850Name",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    saref_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sarefName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    eebus_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "eebusName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sun_spec_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sunSpecName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    hp_bwp_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "hpBwpName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    en17609_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "en17609Name",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class BitmapEntryFunctionalProfile:
    """
    Maps a device-specific bit mask to a literal.
    """
    literal: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class BitmapEntryProduct:
    """
    Maps a device-specific bit mask to a literal.
    """
    literal: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    hex_mask: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "hexMask",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "format": "base16",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ChangeLog:
    """
    document history.
    """
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    author: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class DataDirection(Enum):
    """
    Read/write direction with read (R), write (W), read-write (RW), read-write
    with persistent storage (RWP)
    """
    R = "R"
    W = "W"
    RW = "RW"
    RWP = "RWP"


class DeviceCategory(Enum):
    """
    Device Category is inherited from EEBUS, a growing list of supported
    Devices.

    :cvar BATTERY:
    :cvar COMPRESSOR:
    :cvar DEVICE_INFORMATION:
    :cvar DHWCIRCUIT:
    :cvar DHWSTORAGE:
    :cvar DISHWASHER:
    :cvar DRYER:
    :cvar ELECTRICAL_IMMERSION_HEATER:
    :cvar FAN:
    :cvar GAS_HEATING_APPLIANCE:
    :cvar GENERIC:
    :cvar HEATING_BUFFER_STORAGE:
    :cvar HEATING_CIRCUIT:
    :cvar HEATING_OBJECT:
    :cvar HEATING_ZONE:
    :cvar HEAT_PUMP_APPLIANCE:
    :cvar HEAT_SINK_CIRCUIT:
    :cvar HEAT_SOURCE_CIRCUIT:
    :cvar HEAT_SOURCE_UNIT:
    :cvar HVACCONTROLLER:
    :cvar HVACROOM:
    :cvar INSTANT_DHWHEATER:
    :cvar INVERTER:
    :cvar OIL_HEATING_APPLIANCE:
    :cvar PUMP:
    :cvar REFRIGERANT_CIRCUIT:
    :cvar SMART_ENERGY_APPLIANCE:
    :cvar SOLAR_DHWSTORAGE:
    :cvar SOLAR_THERMAL_CIRCUIT:
    :cvar SUB_METER_ELECTRICITY:
    :cvar TEMPERATURE_SENSOR:
    :cvar WASHER:
    :cvar BATTERY_SYSTEM:
    :cvar ELECTRICITY_GENERATION_SYSTEM:
    :cvar ELECTRICITY_STORAGE_SYSTEM:
    :cvar SGCP: EEBUS: GridConnectionPointOfPremises
    :cvar HOUSEHOLD:
    :cvar PVSYSTEM:
    :cvar EV:
    :cvar EVSE:
    :cvar CHARGING_STATION: EEBUS: ChargingOutlet
    :cvar CEM:
    """
    BATTERY = "Battery"
    COMPRESSOR = "Compressor"
    DEVICE_INFORMATION = "DeviceInformation"
    DHWCIRCUIT = "DHWCircuit"
    DHWSTORAGE = "DHWStorage"
    DISHWASHER = "Dishwasher"
    DRYER = "Dryer"
    ELECTRICAL_IMMERSION_HEATER = "ElectricalImmersionHeater"
    FAN = "Fan"
    GAS_HEATING_APPLIANCE = "GasHeatingAppliance"
    GENERIC = "Generic"
    HEATING_BUFFER_STORAGE = "HeatingBufferStorage"
    HEATING_CIRCUIT = "HeatingCircuit"
    HEATING_OBJECT = "HeatingObject"
    HEATING_ZONE = "HeatingZone"
    HEAT_PUMP_APPLIANCE = "HeatPumpAppliance"
    HEAT_SINK_CIRCUIT = "HeatSinkCircuit"
    HEAT_SOURCE_CIRCUIT = "HeatSourceCircuit"
    HEAT_SOURCE_UNIT = "HeatSourceUnit"
    HVACCONTROLLER = "HVACController"
    HVACROOM = "HVACRoom"
    INSTANT_DHWHEATER = "InstantDHWHeater"
    INVERTER = "Inverter"
    OIL_HEATING_APPLIANCE = "OilHeatingAppliance"
    PUMP = "Pump"
    REFRIGERANT_CIRCUIT = "RefrigerantCircuit"
    SMART_ENERGY_APPLIANCE = "SmartEnergyAppliance"
    SOLAR_DHWSTORAGE = "SolarDHWStorage"
    SOLAR_THERMAL_CIRCUIT = "SolarThermalCircuit"
    SUB_METER_ELECTRICITY = "SubMeterElectricity"
    TEMPERATURE_SENSOR = "TemperatureSensor"
    WASHER = "Washer"
    BATTERY_SYSTEM = "BatterySystem"
    ELECTRICITY_GENERATION_SYSTEM = "ElectricityGenerationSystem"
    ELECTRICITY_STORAGE_SYSTEM = "ElectricityStorageSystem"
    SGCP = "SGCP"
    HOUSEHOLD = "Household"
    PVSYSTEM = "PVSystem"
    EV = "EV"
    EVSE = "EVSE"
    CHARGING_STATION = "ChargingStation"
    CEM = "CEM"


@dataclass
class EmptyType:
    pass


@dataclass
class EnumEntry:
    """
    Maps a device specific ordinal to its literal.
    """
    literal: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    ordinal: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


class Language(Enum):
    """this is the identification of the language for information to be
    published.

    So far en, de, fr and it is possible
    """
    DE = "de"
    EN = "en"
    FR = "fr"
    IT = "it"


class MeasuredValueSource(Enum):
    """
    E0003.
    """
    MEASURED_VALUE = "measuredValue"
    CALCULATED_VALUE = "calculatedValue"
    EMPIRICAL_VALUE = "empiricalValue"


class MeasuredValueType(Enum):
    VALUE = "value"
    MIN = "min"
    MAX = "max"
    AVERAGE = "average"
    STD_DEV = "stdDev"


class ObligLvlType(Enum):
    """E0014: Obligation level of a reaction / function. SHALL: action is required
    SHOULD: action is strongly recommended MAY: action is permitted"""
    OL_SHALL = "OL_SHALL"
    OL_SHOULD = "OL_SHOULD"
    OL_MAY = "OL_MAY"


class PowerSource(Enum):
    """
    E0004.
    """
    UNKNOWN = "unknown"
    MAINS1_PHASE = "mains1Phase"
    MAINS3_PHASE = "mains3Phase"
    BATTERY = "battery"
    DC = "dc"


class PresenceLevel(Enum):
    """
    Indicates wheter the element is mandatory (M), recommended (R, at least one
    of the R elements mus be present), or optional (O, can be ommitted)
    """
    M = "M"
    R = "R"
    O = "O"


class ReleaseState(Enum):
    """
    release state of this XML.
    """
    DRAFT = "Draft"
    REVIEW = "Review"
    PUBLISHED = "Published"
    REVOKED = "Revoked"


class SgcpserviceType(Enum):
    """E0013: Assistance type of a reaction / function. This Attribute indicates the
    type of Flexibility Entity of the operation NET servicable: Operation for the benefit of a
    distribution network operator (DSO) SYS servicable: Operation of the total system operators
    (TSO) ENER servicable: Operation for energy optimization"""
    AT_NET_SERVICEABLE = "AT_NetServiceable"
    AT_SYS_SERVICEABLE = "AT_SysServiceable"
    AT_ENER_SERVICEABLE = "AT_EnerServiceable"


@dataclass
class ScalingFactor:
    """scaled_value = value * multiplicator * 10^powerof10 This type is used for to
    convert intereger datapoint values into floats only"""
    multiplicator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    powerof10: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SmoothTransition:
    """
    The time behavior of a transition from a power adjustment (positive as well
    as negative) can be determined by several time values, so that this starts
    with a random time delay, changes via a ramp and an expiry time with return
    to the initial value.

    :ivar win_tms: indicates a time window in seconds in which the new
        operating mode is started randomly. The time window begins with
        the start command of the operating mode. The value 0 means
        immediate
    :ivar rvrt_tms: determines how long the operating mode should be
        active in seconds. When the time has elapsed, the operating mode
        is automatically terminated. If rvrtTms = 0 (standard value),
        the operating mode remains active until a new command is
        received.
    :ivar rmp_tms: specifies how quickly the changes should be made in
        seconds. The corresponding value is gradually changed from the
        old to the new value in the specified time.
    """
    win_tms: Optional[int] = field(
        default=None,
        metadata={
            "name": "winTms",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rvrt_tms: Optional[int] = field(
        default=None,
        metadata={
            "name": "rvrtTms",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    rmp_tms: Optional[int] = field(
        default=None,
        metadata={
            "name": "rmpTms",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class StabilityFallback:
    """A consumer or a generating system receives the permit for a load change
    for a certain period of time.

    This time is always set to 0 each time a confirmation message is
    received (HeartBeat).

    :ivar max_receive_time: Time in seconds. If the device does not
        recieve any communication within this specified time the device
        automatically initiates the fallback. 0 indicates no fallback
        will be performed.
    :ivar init_value: Value of the reference variable at the start of
        the process cycle. Unit: inherited
    :ivar fallback_value: Value of the reference variable in the event
        of a communication failure . Unit:inherited
    """
    max_receive_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxReceiveTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    init_value: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "initValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    fallback_value: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "fallbackValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class Units(Enum):
    AMPERE_SQUARE_METERS = "AMPERE_SQUARE_METERS"
    AMPERES = "AMPERES"
    AMPERES_PER_METER = "AMPERES_PER_METER"
    AMPERES_PER_SQUARE_METER = "AMPERES_PER_SQUARE_METER"
    BARS = "BARS"
    BTUS = "BTUS"
    BTUS_PER_HOUR = "BTUS_PER_HOUR"
    BTUS_PER_POUND = "BTUS_PER_POUND"
    BTUS_PER_POUND_DRY_AIR = "BTUS_PER_POUND_DRY_AIR"
    CANDELAS = "CANDELAS"
    CANDELAS_PER_SQUARE_METER = "CANDELAS_PER_SQUARE_METER"
    CENTIMETERS = "CENTIMETERS"
    CENTIMETERS_OF_MERCURY = "CENTIMETERS_OF_MERCURY"
    CENTIMETERS_OF_WATER = "CENTIMETERS_OF_WATER"
    CUBIC_FEET = "CUBIC_FEET"
    CUBIC_FEET_PER_MINUTE = "CUBIC_FEET_PER_MINUTE"
    CUBIC_FEET_PER_SECOND = "CUBIC_FEET_PER_SECOND"
    CUBIC_METERS = "CUBIC_METERS"
    CUBIC_METERS_PER_HOUR = "CUBIC_METERS_PER_HOUR"
    CUBIC_METERS_PER_MINUTE = "CUBIC_METERS_PER_MINUTE"
    CUBIC_METERS_PER_SECOND = "CUBIC_METERS_PER_SECOND"
    CURRENCY1 = "CURRENCY1"
    CURRENCY10 = "CURRENCY10"
    CURRENCY2 = "CURRENCY2"
    CURRENCY3 = "CURRENCY3"
    CURRENCY4 = "CURRENCY4"
    CURRENCY5 = "CURRENCY5"
    CURRENCY6 = "CURRENCY6"
    CURRENCY7 = "CURRENCY7"
    CURRENCY8 = "CURRENCY8"
    CURRENCY9 = "CURRENCY9"
    CYCLES_PER_HOUR = "CYCLES_PER_HOUR"
    CYCLES_PER_MINUTE = "CYCLES_PER_MINUTE"
    DAYS = "DAYS"
    DEGREE_DAYS_CELSIUS = "DEGREE_DAYS_CELSIUS"
    DEGREE_DAYS_FAHRENHEIT = "DEGREE_DAYS_FAHRENHEIT"
    DEGREES_ANGULAR = "DEGREES_ANGULAR"
    DEGREES_CELSIUS = "DEGREES_CELSIUS"
    DEGREES_CELSIUS_PER_HOUR = "DEGREES_CELSIUS_PER_HOUR"
    DEGREES_CELSIUS_PER_MINUTE = "DEGREES_CELSIUS_PER_MINUTE"
    DEGREES_FAHRENHEIT = "DEGREES_FAHRENHEIT"
    DEGREES_FAHRENHEIT_PER_HOUR = "DEGREES_FAHRENHEIT_PER_HOUR"
    DEGREES_FAHRENHEIT_PER_MINUTE = "DEGREES_FAHRENHEIT_PER_MINUTE"
    DEGREES_KELVIN = "DEGREES_KELVIN"
    DEGREES_KELVIN_PER_HOUR = "DEGREES_KELVIN_PER_HOUR"
    DEGREES_KELVIN_PER_MINUTE = "DEGREES_KELVIN_PER_MINUTE"
    DEGREES_PHASE = "DEGREES_PHASE"
    DELTA_DEGREES_FAHRENHEIT = "DELTA_DEGREES_FAHRENHEIT"
    DELTA_DEGREES_KELVIN = "DELTA_DEGREES_KELVIN"
    FARADS = "FARADS"
    FEET = "FEET"
    FEET_PER_MINUTE = "FEET_PER_MINUTE"
    FEET_PER_SECOND = "FEET_PER_SECOND"
    FOOT_CANDLES = "FOOT_CANDLES"
    GIGAJOULES = "GIGAJOULES"
    GRAMS_OF_WATER_PER_KILOGRAM_DRY_AIR = "GRAMS_OF_WATER_PER_KILOGRAM_DRY_AIR"
    GRAMS_PER_MINUTE = "GRAMS_PER_MINUTE"
    GRAMS_PER_SECOND = "GRAMS_PER_SECOND"
    HECTOPASCALS = "HECTOPASCALS"
    HENRYS = "HENRYS"
    HERTZ = "HERTZ"
    HORSEPOWER = "HORSEPOWER"
    HOURS = "HOURS"
    HUNDREDTHS_SECONDS = "HUNDREDTHS_SECONDS"
    IMPERIAL_GALLONS = "IMPERIAL_GALLONS"
    IMPERIAL_GALLONS_PER_MINUTE = "IMPERIAL_GALLONS_PER_MINUTE"
    INCHES = "INCHES"
    INCHES_OF_MERCURY = "INCHES_OF_MERCURY"
    INCHES_OF_WATER = "INCHES_OF_WATER"
    JOULE_SECONDS = "JOULE_SECONDS"
    JOULES = "JOULES"
    JOULES_PER_DEGREE_KELVIN = "JOULES_PER_DEGREE_KELVIN"
    JOULES_PER_KILOGRAM_DEGREE_KELVIN = "JOULES_PER_KILOGRAM_DEGREE_KELVIN"
    JOULES_PER_KILOGRAM_DRY_AIR = "JOULES_PER_KILOGRAM_DRY_AIR"
    KILO_BTUS = "KILO_BTUS"
    KILO_BTUS_PER_HOUR = "KILO_BTUS_PER_HOUR"
    KILOGRAMS = "KILOGRAMS"
    KILOGRAMS_PER_CUBIC_METER = "KILOGRAMS_PER_CUBIC_METER"
    KILOGRAMS_PER_HOUR = "KILOGRAMS_PER_HOUR"
    KILOGRAMS_PER_MINUTE = "KILOGRAMS_PER_MINUTE"
    KILOGRAMS_PER_SECOND = "KILOGRAMS_PER_SECOND"
    KILOHERTZ = "KILOHERTZ"
    KILOOHMS = "KILOOHMS"
    KILOJOULES = "KILOJOULES"
    KILOJOULES_PER_DEGREE_KELVIN = "KILOJOULES_PER_DEGREE_KELVIN"
    KILOJOULES_PER_KILOGRAM = "KILOJOULES_PER_KILOGRAM"
    KILOJOULES_PER_KILOGRAM_DRY_AIR = "KILOJOULES_PER_KILOGRAM_DRY_AIR"
    KILOMETERS_PER_HOUR = "KILOMETERS_PER_HOUR"
    KILOPASCALS = "KILOPASCALS"
    KILOVOLT_AMPERES = "KILOVOLT_AMPERES"
    KILOVOLT_AMPERE_HOURS = "KILOVOLT_AMPERE_HOURS"
    KILOVOLT_AMPERES_REACTIVE = "KILOVOLT_AMPERES_REACTIVE"
    KILOVOLT_AMPERES_REACTIVE_HOURS = "KILOVOLT_AMPERES_REACTIVE_HOURS"
    KILOVOLTS = "KILOVOLTS"
    KILOWATT_HOURS = "KILOWATT_HOURS"
    KILOWATTS = "KILOWATTS"
    KW_HOURS_PER_SQUARE_FOOT = "KW_HOURS_PER_SQUARE_FOOT"
    KW_HOURS_PER_SQUARE_METER = "KW_HOURS_PER_SQUARE_METER"
    LITERS = "LITERS"
    LITERS_PER_HOUR = "LITERS_PER_HOUR"
    LITERS_PER_MINUTE = "LITERS_PER_MINUTE"
    LITERS_PER_SECOND = "LITERS_PER_SECOND"
    LUMENS = "LUMENS"
    LUXES = "LUXES"
    MEGA_BTUS = "MEGA_BTUS"
    MEGAHERTZ = "MEGAHERTZ"
    MEGAJOULES = "MEGAJOULES"
    MEGAJOULES_PER_DEGREE_KELVIN = "MEGAJOULES_PER_DEGREE_KELVIN"
    MEGAJOULES_PER_KILOGRAM_DRY_AIR = "MEGAJOULES_PER_KILOGRAM_DRY_AIR"
    MEGAJOULES_PER_SQUARE_FOOT = "MEGAJOULES_PER_SQUARE_FOOT"
    MEGAJOULES_PER_SQUARE_METER = "MEGAJOULES_PER_SQUARE_METER"
    MEGAVOLT_AMPERES = "MEGAVOLT_AMPERES"
    MEGAVOLT_AMPERES_REACTIVE = "MEGAVOLT_AMPERES_REACTIVE"
    MEGAVOLTS = "MEGAVOLTS"
    MEGAWATT_HOURS = "MEGAWATT_HOURS"
    MEGAWATTS = "MEGAWATTS"
    MEGOHMS = "MEGOHMS"
    METERS = "METERS"
    METERS_PER_HOUR = "METERS_PER_HOUR"
    METERS_PER_MINUTE = "METERS_PER_MINUTE"
    METERS_PER_SECOND = "METERS_PER_SECOND"
    METERS_PER_SECOND_PER_SECOND = "METERS_PER_SECOND_PER_SECOND"
    MILES_PER_HOUR = "MILES_PER_HOUR"
    MILLIAMPERES = "MILLIAMPERES"
    MILLIBARS = "MILLIBARS"
    MILLIMETERS = "MILLIMETERS"
    MILLIMETERS_OF_MERCURY = "MILLIMETERS_OF_MERCURY"
    MILLIMETERS_PER_MINUTE = "MILLIMETERS_PER_MINUTE"
    MILLIMETERS_PER_SECOND = "MILLIMETERS_PER_SECOND"
    MILLIOHMS = "MILLIOHMS"
    MILLISECONDS = "MILLISECONDS"
    MILLIVOLTS = "MILLIVOLTS"
    MILLIWATTS = "MILLIWATTS"
    MINUTES = "MINUTES"
    MONTHS = "MONTHS"
    NEWTON = "NEWTON"
    NEWTON_METERS = "NEWTON_METERS"
    NEWTON_SECONDS = "NEWTON_SECONDS"
    NEWTONS_PER_METER = "NEWTONS_PER_METER"
    NO_UNITS = "NO_UNITS"
    OHM_METERS = "OHM_METERS"
    OHMS = "OHMS"
    PARTS_PER_BILLION = "PARTS_PER_BILLION"
    PARTS_PER_MILLION = "PARTS_PER_MILLION"
    PASCALS = "PASCALS"
    PER_HOUR = "PER_HOUR"
    PER_MINUTE = "PER_MINUTE"
    PER_SECOND = "PER_SECOND"
    PERCENT = "PERCENT"
    PERCENT_OBSCURATION_PER_FOOT = "PERCENT_OBSCURATION_PER_FOOT"
    PERCENT_OBSCURATION_PER_METER = "PERCENT_OBSCURATION_PER_METER"
    PERCENT_PER_SECOND = "PERCENT_PER_SECOND"
    PERCENT_RELATIVE_HUMIDITY = "PERCENT_RELATIVE_HUMIDITY"
    POUNDS_FORCE_PER_SQUARE_INCH = "POUNDS_FORCE_PER_SQUARE_INCH"
    POUNDS_MASS = "POUNDS_MASS"
    POUNDS_MASS_PER_HOUR = "POUNDS_MASS_PER_HOUR"
    POUNDS_MASS_PER_MINUTE = "POUNDS_MASS_PER_MINUTE"
    POUNDS_MASS_PER_SECOND = "POUNDS_MASS_PER_SECOND"
    POWER_FACTOR = "POWER_FACTOR"
    PSI_PER_DEGREE_FAHRENHEIT = "PSI_PER_DEGREE_FAHRENHEIT"
    RADIANS = "RADIANS"
    RADIANS_PER_SECOND = "RADIANS_PER_SECOND"
    REVOLUTIONS_PER_MINUTE = "REVOLUTIONS_PER_MINUTE"
    SECONDS = "SECONDS"
    SIEMENS = "SIEMENS"
    SIEMENS_PER_METER = "SIEMENS_PER_METER"
    SQUARE_CENTIMETERS = "SQUARE_CENTIMETERS"
    SQUARE_FEET = "SQUARE_FEET"
    SQUARE_INCHES = "SQUARE_INCHES"
    SQUARE_METERS = "SQUARE_METERS"
    SQUARE_METERS_PER_NEWTON = "SQUARE_METERS_PER_NEWTON"
    TESLAS = "TESLAS"
    THERMS = "THERMS"
    TON_HOURS = "TON_HOURS"
    TONS = "TONS"
    TONS_PER_HOUR = "TONS_PER_HOUR"
    TONS_REFRIGERATION = "TONS_REFRIGERATION"
    US_GALLONS = "US_GALLONS"
    US_GALLONS_PER_MINUTE = "US_GALLONS_PER_MINUTE"
    VOLT_AMPERES = "VOLT_AMPERES"
    VOLT_AMPERES_REACTIVE = "VOLT_AMPERES_REACTIVE"
    VOLTS = "VOLTS"
    VOLTS_PER_DEGREE_KELVIN = "VOLTS_PER_DEGREE_KELVIN"
    VOLTS_PER_METER = "VOLTS_PER_METER"
    WATT_HOURS = "WATT_HOURS"
    WATTS = "WATTS"
    WATTS_PER_METER_PER_DEGREE_KELVIN = "WATTS_PER_METER_PER_DEGREE_KELVIN"
    WATTS_PER_SQUARE_FOOT = "WATTS_PER_SQUARE_FOOT"
    WATTS_PER_SQUARE_METER = "WATTS_PER_SQUARE_METER"
    WATTS_PER_SQUARE_METER_DEGREE_KELVIN = "WATTS_PER_SQUARE_METER_DEGREE_KELVIN"
    WEBERS = "WEBERS"
    WEEKS = "WEEKS"
    YEARS = "YEARS"
    NONE = "NONE"


@dataclass
class VersionNumber:
    """
    a three digit version mumber system.
    """
    primary_version_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "primaryVersionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    secondary_version_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "secondaryVersionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    sub_release_version_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "subReleaseVersionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class EnumEntryProductRecord:
    class Meta:
        name = "enumEntryProductRecord"

    literal: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    ordinal: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class EnumEntryRecordFunctionalProfile:
    class Meta:
        name = "enumEntryRecordFunctionalProfile"

    literal: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class BitmapFunctionalProfile:
    """bitmap for status bits.

    Maps device-specific bit patterns (as hex mask) to literals.
    """
    bitmap_entry: List[BitmapEntryFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "bitmapEntry",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class BitmapProduct:
    """bitmap for status bits.

    Maps device-specific bit patterns (as hex mask) to literals.
    """
    bitmap_entry: List[BitmapEntryProduct] = field(
        default_factory=list,
        metadata={
            "name": "bitmapEntry",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class EnumType:
    """Enum of states.

    Maps device-specific register values (ordinals) to literals.

    :ivar enum_entry:
    :ivar hex_mask: hex mask for bit-wise AND before evaluating the enum
    """
    class Meta:
        name = "Enum"

    enum_entry: List[EnumEntry] = field(
        default_factory=list,
        metadata={
            "name": "enumEntry",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    hex_mask: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "hexMask",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "format": "base16",
        }
    )


@dataclass
class EnumMapFunctionalProfile:
    enum_entry: List[EnumEntryRecordFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "enumEntry",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    hex_mask: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "hexMask",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "format": "base16",
        }
    )


@dataclass
class EnumMapProduct:
    enum_entry: List[EnumEntryProductRecord] = field(
        default_factory=list,
        metadata={
            "name": "enumEntry",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
    hex_mask: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "hexMask",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "format": "base16",
        }
    )


@dataclass
class FlexAssistance:
    assists: Optional[SgcpserviceType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    obliged_to: Optional[ObligLvlType] = field(
        default=None,
        metadata={
            "name": "obligedTo",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class FunctionalProfileIdentification:
    """
    Specification of design source 0 means: specified by SmartGridready, the
    Porfilenumber follows the SmargGirdready scheme &gt;0 means: specfied by
    manufacturer hhhh, the Profilenumber followos a manufacturors scheme.

    :ivar specification_owner_identification:
    :ivar functional_profile_category: The Profile Identfication
        identiofis the main profile classes. The enumeration text is
        also documented with numbers being referenced in the profile
        number hhhh.nnnn.uuuu.ss.VV.vv as nnnn
    :ivar functional_profile_type:
    :ivar level_of_operation: levelOfOperation defines a controls
        complexity level m) for read-only monitoring dat points level 1)
        single contact 2) 2 or more contacts /state controlled interface
        3) statical defined characteristics tables 4) dynamic realtime
        control combined with statical defined characteristics tables 5)
        dynamic realtime control combined with dynamic changeable
        characteristics tables 6) prognosis based systems
    :ivar version_number:
    """
    specification_owner_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "specificationOwnerIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    functional_profile_category: Optional[FunctionalProfileCategory] = field(
        default=None,
        metadata={
            "name": "functionalProfileCategory",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    functional_profile_type: Optional[FunctionalProfileType] = field(
        default=None,
        metadata={
            "name": "functionalProfileType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    level_of_operation: Optional[LevelOfOperation] = field(
        default=None,
        metadata={
            "name": "levelOfOperation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    version_number: Optional[VersionNumber] = field(
        default=None,
        metadata={
            "name": "versionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class LegibleDescription:
    """This element us used to extend the definitions with legible text
    elements: a short understandbale explanation of the items addressed.

    These elements are used for printed and published information

    :ivar text_element: information to be published
    :ivar language: language identifier de, en, fr, it
    :ivar uri: optional URI pointong towards additional information
    """
    text_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "textElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
            "min_length": 0,
            "max_length": 4000,
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    uri: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class ReleaseNotes:
    """
    Contains versioning, history and release states.
    """
    state: Optional[ReleaseState] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    remarks: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    change_log: List[ChangeLog] = field(
        default_factory=list,
        metadata={
            "name": "changeLog",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class DataTypeFunctionalProfile:
    """Generic high-level data types.

    Implementations of this XSD map these types into native data types
    in their programming language (java, python, golang, ...)
    """
    enum: Optional[EnumMapFunctionalProfile] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    bitmap: Optional[BitmapFunctionalProfile] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    boolean: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int8U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int16U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int32U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int64U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    date_time: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "dateTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    string: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class DataTypeProduct:
    """Generic high-ldevel data types.

    Implementations of this XSD map these types into native data types
    in their programming language (java, python, golang, ...)
    """
    enum: Optional[EnumMapProduct] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    bitmap: Optional[BitmapProduct] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    boolean: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int8U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int16U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int32U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64_u: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "int64U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float32: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float64: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    date_time: Optional[EmptyType] = field(
        default=None,
        metadata={
            "name": "dateTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    string: Optional[EmptyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class GenericAttributes:
    """these attributes are defined for the generic interface for the
    application programmer.

    An attribute can be aligned to either a device, a functional Profile
    or a datapoint

    :ivar max_val: upper range limit. Unit:inherited
    :ivar min_val: lower range limit. Unit:inherited
    :ivar special_quality_requirement: indicates quality requirements
        fullfilled like formal certifications
    :ivar precision_percent: the precisionPercent of a measurement,
        calculation result or result of a controls process
    :ivar stability_fallback: A consumer or a generating system receives
        the permit for a load change for a certain period of time. This
        time is always set to 0 each time a confirmation message is
        received (HeartBeat).
    :ivar smooth_transition: The time behavior of a transition from a
        power adjustment (positive as well as negative) can be
        determined by several time values, so that this starts with a
        random time delay, changes via a ramp and an expiry time with
        return to the initial value.
    :ivar max_latency_time_ms: Maximum time in milliseconds from
        capturing of measured value until ready at the product interface
        (i.e. analog-digital conversion time)
    :ivar measured_value_type: MeasValueType: type of measurement.
        Possbile values are "value", "min", max", "average", "stdDev"
    :ivar measured_value_source: Value source kind related to SGr level
        6 applications. Potential values are measuredValue,
        calculatedValue, empiricalValue
    :ivar sample_rate_hz: SampleRate in Hertz
    :ivar curtailment:
    :ivar min_load:
    :ivar max_lock_time_minutes:
    :ivar min_run_time_minutes:
    :ivar value_by_time_table_minutes:
    :ivar flex_assistance: Systems with more than One communicator need
        a definition of the priority of the commands / demands for a
        flexibility requirement. This element defines the kind of a such
        a command (servicable for net (DSO), energy or system (TNO)) and
        its priority (SHALL / SHOULD / MAY)
    :ivar unit_conversion_multiplicator:
    """
    max_val: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "maxVal",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    min_val: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "minVal",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    special_quality_requirement: Optional[str] = field(
        default=None,
        metadata={
            "name": "specialQualityRequirement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    precision_percent: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "precisionPercent",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_inclusive": Decimal("0.001"),
            "max_inclusive": Decimal("15"),
        }
    )
    stability_fallback: Optional[StabilityFallback] = field(
        default=None,
        metadata={
            "name": "stabilityFallback",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    smooth_transition: Optional[SmoothTransition] = field(
        default=None,
        metadata={
            "name": "smoothTransition",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    max_latency_time_ms: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxLatencyTimeMs",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    measured_value_type: Optional[MeasuredValueType] = field(
        default=None,
        metadata={
            "name": "measuredValueType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    measured_value_source: Optional[MeasuredValueSource] = field(
        default=None,
        metadata={
            "name": "measuredValueSource",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sample_rate_hz: Optional[int] = field(
        default=None,
        metadata={
            "name": "sampleRateHz",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    curtailment: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    min_load: Optional[float] = field(
        default=None,
        metadata={
            "name": "minLoad",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    max_lock_time_minutes: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxLockTimeMinutes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    min_run_time_minutes: Optional[float] = field(
        default=None,
        metadata={
            "name": "minRunTimeMinutes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    value_by_time_table_minutes: Optional[float] = field(
        default=None,
        metadata={
            "name": "valueByTimeTableMinutes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    flex_assistance: Optional[FlexAssistance] = field(
        default=None,
        metadata={
            "name": "flexAssistance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    unit_conversion_multiplicator: Optional[float] = field(
        default=None,
        metadata={
            "name": "unitConversionMultiplicator",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
