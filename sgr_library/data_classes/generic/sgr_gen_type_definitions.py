from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class SgreadyStateLv1Type(Enum):
    """
    E0006 simple heat pump blocking association bwp normal,EVU_LOCK.

    :cvar HP_NORMAL: Normal operation, optimized according to customer
        requirements
    :cvar HP_LOCK: Locked operation for a maximum of 2 hours
    """
    HP_NORMAL = "HP_NORMAL"
    HP_LOCK = "HP_LOCK"


class SgreadyStateLv2Type(Enum):
    """
    E0005 SG-Ready states according the German heatpump association bwp normal,
    intensivied, EVU_LOCK, forced https://www.waermepumpe.de/normen-technik/sg-
    ready/

    :cvar HP_NORMAL: Normal operation, optimized according to customer
        requirements
    :cvar HP_INTENSIVIED: Increased operation
    :cvar HP_LOCKED: Locked operation for a maximum of 2 hours
    :cvar HP_FORCED: Start command
    """
    HP_NORMAL = "HP_NORMAL"
    HP_INTENSIVIED = "HP_INTENSIVIED"
    HP_LOCKED = "HP_LOCKED"
    HP_FORCED = "HP_FORCED"


@dataclass
class SgrChangeLog:
    class Meta:
        name = "SGrChangeLog"

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


class SgrDeviceKindType(Enum):
    """
    Device Kind is inherited from EEBUS, a growing list of supported Devices.

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


class SgrEvsestateLv1Type(Enum):
    """E0009 : 0 = EV_NORMAL, 1 = EV_REDUCED"""
    EV_NORMAL = "EV_NORMAL"
    EV_REDUCED = "EV_REDUCED"


class SgrEvsestateLv2Type(Enum):
    """E0008 : 0:0 = EV_NORMAL, 0:1 = EV_REDUCED , 1:0 =
    EV_MINIMAL , 1:1 = EV_NONE_OR_FEEDIN"""
    EV_NORMAL = "EV_NORMAL"
    EV_REDUCED = "EV_REDUCED"
    EV_MINIMAL = "EV_MINIMAL"
    EV_NONE_OR_FEEDIN = "EV_NONE_OR_FEEDIN"


class SgrEvstateType(Enum):
    """E0012 IEC EVSE_61851_State  for Wallbox
    A: standby,
    B: vehicle detected,
    C: ready (charging),
    D: with ventilation,
    E: no power (shut off),
    F: error"""
    EV_STATE_UNDEF = "EV_STATE_UNDEF"
    EV_STANDBY = "EV_STANDBY"
    EV_DETECTED = "EV_DETECTED"
    EV_READY4_CHARGING = "EV_READY4CHARGING"
    EV_WITHFAN = "EV_WITHFAN"
    EV_SHUTOFF = "EV_SHUTOFF"
    EV_ERROR = "EV_ERROR"


class SgrHpopModeType(Enum):
    """E0016:
    Basic operation type of a heat pump
    Bereitschaft, Programm, Komfort, Eco, Warmwasser, Notbetrieb"""
    WP_EMERG_OP = "WP_EMERG_OP"
    WP_READY = "WP_READY"
    WP_PROG_OP = "WP_PROG_OP"
    WP_COMFORT_OP = "WP_COMFORT_OP"
    WP_ECO_OP = "WP_ECO_OP"
    WP_DOM_WATER_OP = "WP_DOM_WATER_OP"


class SgrLanguageType(Enum):
    """this is the identification of the language for information to be
    published.

    So far en, de, fr and it is possible
    """
    DE = "de"
    EN = "en"
    FR = "fr"
    IT = "it"


class SgrMropresenceLevelIndicationType(Enum):
    """
    Names for the presence indication of Elements listed in the tables are
    defined as follows (using the EEBUS terminology): "M" mandatotory use
    (IEC:SHALL), "R" recommended use (IEC:SHOULD) and "O" optional use
    (IEC:MAY)
    """
    M = "M"
    R = "R"
    O = "O"


class SgrMeasValueSourceType(Enum):
    """
    E0003.
    """
    MEASURED_VALUE = "measuredValue"
    CALCULATED_VALUE = "calculatedValue"
    EMPIRICAL_VALUE = "empiricalValue"


class SgrMeasValueType(Enum):
    VALUE = "value"
    MIN = "min"
    MAX = "max"
    AVERAGE = "average"
    STD_DEV = "stdDev"


@dataclass
class SgrNamelistType:
    """a list of relevant namespaces list for to display names used in
    different standards like EEBUS, IEC6850,, SAREF4ENER etc this list type is
    used for devices, functional profiles and datapoints.

    This namespace naming framework is typically used by the SGr
    association in order to tailer web based information tools. This
    complex data type is intended to be extended for future relevant
    standarrds in order to secure information over technology live
    cycles List der für ein Profil relevanten Namen von benutzten
    Standards

    :ivar s_lv1_name: names used for SGr label V1 used to secure legacy
        compatibility
    :ivar s_work_name: work names for temporary use
    :ivar s_manuf_name: manufacturers may use an internal wording
    :ivar s_iec61850_name: IEC 61850 termonoligy place to add the 61850
        abreviatuions if an overlap exists
    :ivar s_sarefname: SAREF for ENER termonoligy place to add the SAREF
        abreviations if an overlap exists
    :ivar s_eebusname: EEBUS for terminology place to add the EEBUS
        abreviations if an overlap exists
    :ivar s_hpbwp_name: bwp (German Heat Pump Association) for
        terminology place to add the bwp naming for HVAC if an overlap
        exists
    """
    class Meta:
        name = "SGrNamelistType"

    s_lv1_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sLV1Name",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_work_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sWorkName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_manuf_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sManufName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_iec61850_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sIEC61850Name",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_sarefname: Optional[str] = field(
        default=None,
        metadata={
            "name": "sSAREFName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_eebusname: Optional[str] = field(
        default=None,
        metadata={
            "name": "sEEBUSName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    s_hpbwp_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sHPbwpName",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


class SgrOcppstateType(Enum):
    """E0015:
    Available (0):
    When a Connector becomes available for a new
    user (Operative)
    Charging (1):
    When the contactor of a Connector closes,
    allowing the vehicle to charge
    (Operative)
    Preparing(not yet observed ?):
    When a Connector becomes no longer available
    for a new user but no charging session is active.
    Typically a Connector is occupied when a user
    presents a tag, inserts a cable or a vehicle
    occupies the parking bay
    (Operative)
    Finishing(not yet observed ?):
    When a charging session has stopped at a
    Connector, but the Connector is not yet available
    for a new user, e.g. the cable has not been
    removed or the vehicle has not left the parking
    bay
    (Operative)
    Reserved(not yet observed ?):
    When a Connector becomes reserved as a result of
    a Reserve Now command
    (Operative)
    Unavailable(not yet observed ?):
    When a Connector becomes unavailable as the
    result of a Change Availability command or an
    event upon which the Charge Point transitions to
    unavailable at its discretion. Upon receipt of a
    Change Availability command, the status MAY
    change immediately or the change MAY be
    scheduled. When scheduled, the Status
    Notification shall be send when the availability
    change becomes effective
    (Inoperative)
    Faulted(not yet observed ?):
    When a Charge Point or connector has reported
    an error and is not available for energy delivery .
    (Inoperative).
    SuspendedEVSE (7):
    When the contactor of a Connector opens upon
    request of the EVSE, e.g. due to a smart charging
    restriction or as the result of
    StartTransaction.conf indicating that charging is
    not allowed
    (Operative)
    SuspendedEV(8):
    When the EVSE is ready to deliver energy but
    contactor is open, e.g. the EV is not ready.
    (Operative)"""
    AVAILABLE = "Available"
    CHARGING = "Charging"
    PREPARING = "Preparing"
    FINISHING = "Finishing"
    RESERVED = "Reserved"
    UNAVAILABLE = "Unavailable"
    FAULTED = "Faulted"
    SUSPENDED_EVSE = "SuspendedEVSE"
    SUSPENDED_EV = "SuspendedEV"


class SgrObligLvlType(Enum):
    """E0014:  Obligation level of a reaction / function.
    SHALL:  action is required
    SHOULD: action is strongly recommended
    MAY: action is permitted"""
    OL_SHALL = "OL_SHALL"
    OL_SHOULD = "OL_SHOULD"
    OL_MAY = "OL_MAY"


class SgrPowerSourceType(Enum):
    """
    E0004.
    """
    UNKNOWN = "unknown"
    MAINS1_PHASE = "mains1Phase"
    MAINS3_PHASE = "mains3Phase"
    BATTERY = "battery"
    DC = "dc"


class SgrRwptype(Enum):
    """Names for the data direction indication.

    "R" read only data, "W" rite only data, "RW" readible and writable
    data, "RWP" readible and writable data with persistent storage
    """
    R = "R"
    W = "W"
    RW = "RW"
    RWP = "RWP"


class SgrReleaseState(Enum):
    DRAFT = "Draft"
    REVIEW = "Review"
    PUBLISHED = "Published"
    REVOKED = "Revoked"


class SgrSgcpfeedInStateLv2Type(Enum):
    """E0011 : 0:0 = FI_NORMAL, 0:1 = FI_REDUCED , 1:0 =
    FI_LOCKED , 1:1 = FI_MAX"""
    FI_NORMAL = "FI_NORMAL"
    FI_REDUCED = "FI_REDUCED"
    FI_LOCKED = "FI_LOCKED"
    FI_MAX = "FI_MAX"


class SgrSgcploadStateLv2Type(Enum):
    """E0010 : 0:0 = LD_NORMAL, 0:1 = LD_REDUCED , 1:0 =
    LD_LOCKED , 1:1 = LD_MAX"""
    LD_NORMAL = "LD_NORMAL"
    LD_REDUCED = "LD_REDUCED"
    LD_LOCKED = "LD_LOCKED"
    LD_MAX = "LD_MAX"


class SgrSgcpserviceType(Enum):
    """E0013: Assistance type of a reaction / function. This Attribute indicates the type of Flexibility Entity of the operation
    NET  servicable: Operation for the benefit of a distribution network operator (DSO)
    SYS  servicable: Operation of the total system operators (TSO)
    ENER servicable: Operation for energy optimization"""
    AT_NET_SERVICABLE = "AT_NetServicable"
    AT_SYS_SERVICABLE = "AT_SysServicable"
    AT_ENER_SERVICABLE = "AT_EnerServicable"


@dataclass
class SgrScalingType:
    """scaled_value = value * multiplicator * 10^powerof10
    This type is used for to convert intereger datapoint values into
    floats only"""
    class Meta:
        name = "SGrScalingType"

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
class SgrSmoothTransitionType:
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
    class Meta:
        name = "SGrSmoothTransitionType"

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
class SgrStabilityFallbackType:
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
    class Meta:
        name = "SGrStabilityFallbackType"

    max_receive_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxReceiveTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    init_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "initValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    fallback_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "fallbackValue",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


class SgrSunspStateCodesType(Enum):
    """E0007 : SunspecInvStates I_STATUS_OFF,
    I_STATUS_SLEEPING , I_STATUS_STARTING ,I_STATUS_MPPT ,
    I_STATUS_THROTTLED, I_STATUS_SHUTING_DOWN ,I_STATUS_FAULT ,
    I_STATUS_STANDBY"""
    I_STATUS_OFF = "I_STATUS_OFF"
    I_STATUS_SLEEPING = "I_STATUS_SLEEPING"
    I_STATUS_STARTING = "I_STATUS_STARTING"
    I_STATUS_MPPT = "I_STATUS_MPPT"
    I_STATUS_THROTTLED = "I_STATUS_THROTTLED"
    I_STATUS_SHUTING_DOWN = "I_STATUS_SHUTING_DOWN"
    I_STATUS_FAULT = "I_STATUS_FAULT"
    I_STATUS_STANDBY = "I_STATUS_STANDBY"


class SgrTransportServicesUsedListType(Enum):
    EEBUS = "EEBUS"
    MODBUS = "Modbus"
    OCPP1_6 = "OCPP1.6"
    OCPP2_01 = "OCPP2.01"
    RESTFUL_JSON = "RESTfulJSON"
    CONTACTS = "Contacts"
    WO_T = "WoT"
    PROPRIETARY = "proprietary"
    GENERIC = "generic"


class SgrUnits(Enum):
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
    KILOVOLT_AMPERES_REACTIVE = "KILOVOLT_AMPERES_REACTIVE"
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
class SgrVersionNumberType:
    """
    a three digit version mumber system.
    """
    class Meta:
        name = "SGrVersionNumberType"

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
class SgrEnumListType:
    class Meta:
        name = "SGrEnumListType"

    sgr_meas_value_source: Optional[SgrMeasValueSourceType] = field(
        default=None,
        metadata={
            "name": "sgrMeasValueSource",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_power_source: Optional[SgrPowerSourceType] = field(
        default=None,
        metadata={
            "name": "sgrPowerSource",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgready_state_lv2: Optional[SgreadyStateLv2Type] = field(
        default=None,
        metadata={
            "name": "sgreadyStateLv2",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgready_state_lv1: Optional[SgreadyStateLv1Type] = field(
        default=None,
        metadata={
            "name": "sgreadyStateLv1",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_sunsp_state_codes: Optional[SgrSunspStateCodesType] = field(
        default=None,
        metadata={
            "name": "sgrSunspStateCodes",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_evsestate_lv2: Optional[SgrEvsestateLv2Type] = field(
        default=None,
        metadata={
            "name": "sgrEVSEStateLv2",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_evsestate_lv1: Optional[SgrEvsestateLv1Type] = field(
        default=None,
        metadata={
            "name": "sgrEVSEStateLv1",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_sgcpload_state_lv2: Optional[SgrSgcploadStateLv2Type] = field(
        default=None,
        metadata={
            "name": "sgrSGCPLoadStateLv2",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_sgcpfeed_in_state_lv2: Optional[SgrSgcpfeedInStateLv2Type] = field(
        default=None,
        metadata={
            "name": "sgrSGCPFeedInStateLv2",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_evstate: Optional[SgrEvstateType] = field(
        default=None,
        metadata={
            "name": "sgrEVState",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_sgcpservice: Optional[SgrSgcpserviceType] = field(
        default=None,
        metadata={
            "name": "sgrSGCPService",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_oblig_lvl: Optional[SgrObligLvlType] = field(
        default=None,
        metadata={
            "name": "sgrObligLvl",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_ocppstate: Optional[SgrOcppstateType] = field(
        default=None,
        metadata={
            "name": "sgrOCPPState",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sgr_hpop_mode: Optional[SgrHpopModeType] = field(
        default=None,
        metadata={
            "name": "sgrHPOpMode",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrFlexAssistanceType:
    class Meta:
        name = "SGrFlexAssistanceType"

    assists: Optional[SgrSgcpserviceType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    obliged_to: Optional[SgrObligLvlType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SgrLegibDocumentationType:
    """This element us used to extend the definitions with legible text
    elements: a short understandbale explanation of the items addressed.

    These elements are used for printed and published information

    :ivar text_element: information to be published
    :ivar language: language identifier de, en, fr, it
    :ivar uri: URI pointong towards additional information
    """
    class Meta:
        name = "SGrLegibDocumentationType"

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
    language: Optional[SgrLanguageType] = field(
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
class SgrReleaseNotes:
    """
    Contains versioning, history and release states.
    """
    class Meta:
        name = "SGrReleaseNotes"

    state: Optional[SgrReleaseState] = field(
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
    changelog: List[SgrChangeLog] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_occurs": 1,
        }
    )


@dataclass
class SgrAttr4GenericType:
    """these attributes are defined for the generic interface for the
    application programmer.

    An attribute can be aligned to either a device, a functional Profile
    or a datapoint

    :ivar max_val: upper range limit. Unit:inherited
    :ivar min_val: lower range limit. Unit:inherited
    :ivar spec_quality_requirement: indicates Quality requirements
        fullfilled like formal certifications
    :ivar precision: the precision of a measurement, calculation result
        or result of a controls process
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
        capturing of measured value until ready at the external
        interface (i.e. analog-digital conversion time)
    :ivar value_type: MeasValueType: type of measurement. Possbile
        values are "value", "min", max", "average", "stdDev"
    :ivar value_source: Value source kind related to SGr level 6
        applications. Potential values are measuredValue,
        calculatedValue, empiricalValue
    :ivar sample_rate: SampleRate in milliseconds
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
    """
    class Meta:
        name = "SGrAttr4GenericType"

    max_val: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxVal",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    min_val: Optional[float] = field(
        default=None,
        metadata={
            "name": "minVal",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    spec_quality_requirement: Optional[str] = field(
        default=None,
        metadata={
            "name": "specQualityRequirement",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    precision: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "min_inclusive": 0.001,
            "max_inclusive": 15.0,
        }
    )
    stability_fallback: Optional[SgrStabilityFallbackType] = field(
        default=None,
        metadata={
            "name": "stabilityFallback",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    smooth_transition: Optional[SgrSmoothTransitionType] = field(
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
    value_type: Optional[SgrMeasValueType] = field(
        default=None,
        metadata={
            "name": "valueType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    value_source: Optional[SgrMeasValueSourceType] = field(
        default=None,
        metadata={
            "name": "valueSource",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    sample_rate: Optional[int] = field(
        default=None,
        metadata={
            "name": "sampleRate",
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
    flex_assistance: Optional[SgrFlexAssistanceType] = field(
        default=None,
        metadata={
            "name": "flexAssistance",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrBasicGenDataPointTypeType:
    """These are the basic generic data types must remain high level
    definitions for to be supported.

    The definition focuses on the programming languages used at the
    level of the communicators. So far Java and Python.
    """
    class Meta:
        name = "SGrBasicGenDataPointTypeType"

    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int8_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "int8U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int16_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "int16U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int32_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "int32U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    int64_u: Optional[int] = field(
        default=None,
        metadata={
            "name": "int64U",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float32: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    float64: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    enum: Optional[SgrEnumListType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dateTime",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    string: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )


@dataclass
class SgrBasicGenArrayDptypeType:
    """These are the basic generic data array  types must remain high level
    definitions for to be supported.

    The definition focuses on the programming languages used at the
    level of the communicators. So far Java and Python.
    """
    class Meta:
        name = "SGrBasicGenArrayDPTypeType"

    type: Optional[SgrBasicGenDataPointTypeType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    lenght: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
