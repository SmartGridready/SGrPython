from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate
from sgrspecification.generic.base_type_functional_profile_category import FunctionalProfileCategory
from sgrspecification.generic.base_type_level_of_operation_type import LevelOfOperation

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class AlternativeNames:
    """a name list for EEBUS, IEC6850,, SAREF4ENER etc.

    Used to support ontology naming.

    :ivar s_lv1_name: Currently not used. Reserved for the future to
        secure legacy compatibility one we start renaming in future SGr
        label versions
    :ivar work_name: work name for temporary use
    :ivar manuf_name: manufacturers may use an internal wording
    :ivar iec61850_name: IEC 61850 terminology place to add the 61850
        abbreviatuions
    :ivar saref_name: SAREF for ENER terminology place to add the SAREF
        abbreviations (https://saref.etsi.org)
    :ivar eebus_name: EEBUS for terminology place to add the EEBUS
        abbreviations
    :ivar sun_spec_name: sSUNSPEC for terminology place to add the
        www.sunspec.org abbreviations
    :ivar hp_bwp_name: bwp (German Heat Pump Association) for
        terminology place to add the bwp naming for HVAC
    :ivar en17609_name: EN17609 terminology place to add the EU17609
        abbreviations
    """
    s_lv1_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sLV1Name",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
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


class DataDirectionFunctionalProfile(Enum):
    """
    Read/write direction with read (R), write (W), read-write (RW)
    """
    R = "R"
    W = "W"
    RW = "RW"


class DataDirectionProduct(Enum):
    """
    Read/write direction with read (R), write (W), read-write (RW), read-write
    with persistent storage (RWP), or constant (C)
    """
    C = "C"
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
    :cvar ACTUATOR:
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
    ACTUATOR = "Actuator"
    CEM = "CEM"


@dataclass
class EmptyType:
    pass


class EmptyValue(Enum):
    VALUE = ""


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


@dataclass
class EnumEntryProductRecord:
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
class GenericAttributeFunctionalProfile:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
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
    Indicates whether the element is mandatory (M), recommended (R, at least
    one of the R elements must be present), or optional (O, can be omitted)
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


@dataclass
class ScalingFactor:
    """scaled_value = value * multiplicator * 10^powerof10 This type is used for to
    convert integer datapoint values into floats only"""
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


class Units(Enum):
    AMPERES = "AMPERES"
    BARS = "BARS"
    CUBIC_METERS = "CUBIC_METERS"
    CUBIC_METERS_PER_SECOND = "CUBIC_METERS_PER_SECOND"
    DEGREES_CELSIUS = "DEGREES_CELSIUS"
    DEGREES_PHASE = "DEGREES_PHASE"
    HERTZ = "HERTZ"
    HOURS = "HOURS"
    JOULES = "JOULES"
    KILOGRAMS = "KILOGRAMS"
    KILOVOLT_AMPERES = "KILOVOLT_AMPERES"
    KILOVOLT_AMPERE_HOURS = "KILOVOLT_AMPERE_HOURS"
    KILOVOLT_AMPERES_REACTIVE = "KILOVOLT_AMPERES_REACTIVE"
    KILOVOLT_AMPERES_REACTIVE_HOURS = "KILOVOLT_AMPERES_REACTIVE_HOURS"
    KILOWATT_HOURS = "KILOWATT_HOURS"
    KILOWATTS = "KILOWATTS"
    MEGAWATT_HOURS = "MEGAWATT_HOURS"
    METERS = "METERS"
    METERS_PER_SECOND = "METERS_PER_SECOND"
    METERS_PER_SECOND_PER_SECOND = "METERS_PER_SECOND_PER_SECOND"
    MINUTES = "MINUTES"
    NO_UNITS = "NO_UNITS"
    OHMS = "OHMS"
    PARTS_PER_MILLION = "PARTS_PER_MILLION"
    PASCALS = "PASCALS"
    PER_HOUR = "PER_HOUR"
    PERCENT = "PERCENT"
    PERCENT_RELATIVE_HUMIDITY = "PERCENT_RELATIVE_HUMIDITY"
    POWER_FACTOR = "POWER_FACTOR"
    RADIANS = "RADIANS"
    RADIANS_PER_SECOND = "RADIANS_PER_SECOND"
    REVOLUTIONS_PER_MINUTE = "REVOLUTIONS_PER_MINUTE"
    SECONDS = "SECONDS"
    SQUARE_METERS = "SQUARE_METERS"
    VOLT_AMPERES = "VOLT_AMPERES"
    VOLT_AMPERES_REACTIVE = "VOLT_AMPERES_REACTIVE"
    VOLTS = "VOLTS"
    WATT_HOURS = "WATT_HOURS"
    WATTS = "WATTS"
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
class FunctionalProfileIdentification:
    """
    Specification of design source 0 means: specified by SmartGridready, the
    Profile number follows the SmargGirdready scheme &gt;0 means: specified by
    manufacturer hhhh, the Profile number follows a manufacturers scheme.

    :ivar specification_owner_identification:
    :ivar functional_profile_category: The Profile Identification
        identifies the main profile classes. The enumeration text is
        also documented with numbers being referenced in the profile
        number hhhh.nnnn.uuuu.ss.VV.vv as nnnn
    :ivar functional_profile_type:
    :ivar level_of_operation: levelOfOperation defines a controls
        complexity level m) for read-only monitoring data points level
        1) single contact 2) 2 or more contacts /state controlled
        interface 3) statistical defined characteristics tables 4)
        dynamic real-time control combined with statistical defined
        characteristics tables 5) dynamic real-time control combined
        with dynamic changeable characteristics tables 6) prediction
        based systems
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
    functional_profile_type: Optional[str] = field(
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
class GenericAttributeListFunctionalProfile:
    generic_attribute_list_element: List[GenericAttributeFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "name": "genericAttributeListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class JsonElemFunctionalProfile:
    class Meta:
        name = "JSonElemFunctionalProfile"

    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    date: Optional[EmptyValue] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    string: Optional[EmptyValue] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    number: Optional[EmptyValue] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class LegibleDescription:
    """This element us used to extend the definitions with legible text
    elements: a short understandable explanation of the items addressed.

    These elements are used for printed and published information

    :ivar text_element: information to be published
    :ivar language: language identifier de, en, fr, it
    :ivar uri: optional URI pointing towards additional information
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
class DataTypeProduct:
    """Generic high-devel data types.

    Implementations of this XSD map these types into native data types
    in their programming language (java, python, go lang, ...)
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
    json: Optional[EmptyValue] = field(
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
class JsonArrayOutputFunctionalProfile:
    class Meta:
        name = "JSonArrayOutputFunctionalProfile"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    array: List["JsonArrayOutputFunctionalProfile"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "sequential": True,
        }
    )
    elem: List[JsonElemFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "sequential": True,
        }
    )


@dataclass
class RequestParam:
    param: List[JsonElemFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class GenericAttributeProductEnd:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    data_type: Optional[DataTypeProduct] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    unit: Optional[Units] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class JsonOutputFunctionalProfile:
    class Meta:
        name = "JSonOutputFunctionalProfile"

    array: List[JsonArrayOutputFunctionalProfile] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    elem: List[JsonElemFunctionalProfile] = field(
        default_factory=list,
        metadata={
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
    json: Optional[JsonOutputFunctionalProfile] = field(
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
class GenericAttributeListProductEnd:
    generic_attribute_list_element: List[GenericAttributeProductEnd] = field(
        default_factory=list,
        metadata={
            "name": "genericAttributeListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class GenericAttributeProduct:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    data_type: Optional[DataTypeProduct] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    unit: Optional[Units] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    generic_attribute_list: Optional[GenericAttributeListProductEnd] = field(
        default=None,
        metadata={
            "name": "genericAttributeList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class GenericAttributeListProduct:
    generic_attribute_list_element: List[GenericAttributeProduct] = field(
        default_factory=list,
        metadata={
            "name": "genericAttributeListElement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )
