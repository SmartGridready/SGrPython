from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from sgr_library.data_classes.generic.sgr_gen_type_definitions import (
    SgrLegibDocumentationType,
    SgrMropresenceLevelIndicationType,
    SgrNamelistType,
    SgrVersionNumberType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class ProfileTypeEnumType(Enum):
    """
    :cvar BATTERY: 1: Batterie
    :cvar COMPRESSOR: 2: Kompressor
    :cvar DEVICE_INFORMATION: 3: Geräteinformation
    :cvar DHWCIRCUIT: 4: WarmWasserHeizung
    :cvar DHWSTORAGE: 5: WarmWasserSpeicher
    :cvar DISHWASHER: 6: Geschirrspülmaschine
    :cvar DRYER: 7: Trockner
    :cvar ELECTRICAL_IMMERSION_HEATER: 8: elTauchSieder
    :cvar FAN: 9: Ventilator
    :cvar GAS_HEATING_APPLIANCE: 10: GasWärmeAnwendung
    :cvar NON_SPECIFIC: 11: allgemein verwendbar
    :cvar HEATING_BUFFER_STORAGE: 12: WaermeBufferSpeicher
    :cvar HEATING_CIRCUIT: 13: Heizkreis
    :cvar HEATING_OBJECT: 14: Heizungsobjekt
    :cvar HEATING_ZONE: 15: Heizzone
    :cvar HEAT_PUMP_CONTROL: 16: WärmePumpenAnwendung
    :cvar HEAT_SINK_CIRCUIT: 17: KuehlKoerperSchaltung
    :cvar HEAT_SOURCE_CIRCUIT: 18: WärmekörperSchaltung
    :cvar HEAT_SOURCE_UNIT: 19: Wärmequelle
    :cvar HVACCONTROLLER: 20: HLKController
    :cvar HVACROOM: 21: HLKRaum
    :cvar INSTANT_DHWHEATER: 22: DurchflussWarmwasserHeizung
    :cvar INVERTER: 23: Wechselrichter / Wandler
    :cvar OIL_HEATING_APPLIANCE: 24: OelWaermeAnwendung
    :cvar PUMP: 25: Pumpe
    :cvar REFRIGERANT_CIRCUIT: 26: Kältemittelkreislauf
    :cvar SMART_ENERGY_APPLIANCE: 27: SmartEnergyAppliance
    :cvar SOLAR_DHWSTORAGE: 28: SolarWarmwasserSpeicher
    :cvar SOLAR_THERMAL_CIRCUIT: SolarWarmwasserKreislauf
    :cvar SUB_METER_ELECTRICITY: 30: SubMeter Elektrisch
    :cvar TEMPERATURE_SENSOR: 31: Temperatursensor
    :cvar WASHER: 32: Waschmaschine
    :cvar BATTERY_SYSTEM: 33: Batteriesystem
    :cvar ELECTRICITY_GENERATION_SYSTEM: 34: Generator Elektrisch
    :cvar ELECTRICITY_STORAGE_SYSTEM: 35: ElektroSpeicher System
    :cvar SGCP: 31: GridConnectionPoint Nachbarschaft
    :cvar HOUSEHOLD: 327: Haushalt
    :cvar PVSYSTEM: 38: PV System
    :cvar EV: 39: Elektromobil
    :cvar EVSE: 40: Ladestationscontroller für Elektrofahrzeug
    :cvar CHARGING_OUTLET: 41: Ladestation
    :cvar CEM: 42: Energiemanager für Endverbraucher
    :cvar ACTUATOR: 43:allgemein fuer Aktor
    :cvar SENSOR: 44: allgemein fuer Messdatenaufnahme
    :cvar CONTROLLER: 45:Steuergeraet
    :cvar ENV_CONDITION: 46:Umweltbedingungen
    :cvar FLEX_BUILDING_CAMPUS: 47: Gebäude und Campus.elektrische
        Flexibilität
    :cvar R48: 48: Reserve
    :cvar R49: 49: Reserve
    :cvar R50: 50: Reserve
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
    NON_SPECIFIC = "NonSpecific"
    HEATING_BUFFER_STORAGE = "HeatingBufferStorage"
    HEATING_CIRCUIT = "HeatingCircuit"
    HEATING_OBJECT = "HeatingObject"
    HEATING_ZONE = "HeatingZone"
    HEAT_PUMP_CONTROL = "HeatPumpControl"
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
    CHARGING_OUTLET = "ChargingOutlet"
    CEM = "CEM"
    ACTUATOR = "Actuator"
    SENSOR = "Sensor"
    CONTROLLER = "Controller"
    ENV_CONDITION = "EnvCondition"
    FLEX_BUILDING_CAMPUS = "FlexBuildingCampus"
    R48 = "R48"
    R49 = "R49"
    R50 = "R50"


class SubProfileTypeEnumType(Enum):
    """
    :cvar UNDEF: 0: not yet defined
    :cvar ACTIVE_ENERGY_AC: 1: WirkEnergie
    :cvar REACTIVE_ENERGY_AC: 2:
    :cvar APPARENT_ENERGY_AC: 3:
    :cvar ACTIVE_POWER_AC: 4:
    :cvar REACTIVE_POWER_AC: 5:
    :cvar APPARENT_POWER_AC: 6:
    :cvar VOLTAGE_AC: 7:
    :cvar CURRENT_AC: 8:
    :cvar POWER_FACTOR: 9:
    :cvar PHASE_ANGLE: 10:
    :cvar CURRENT_QUADRANT: 11:
    :cvar FREQUENCY: 12:
    :cvar ACTIVE_ENER_BALANCE_AC: 13:
    :cvar REACTIVE_ENER_BALANCE_AC: 14:
    :cvar CURRENT_DIRECTION: 15:
    :cvar POWER_QUADRANT: 16:
    :cvar ENERGY_DC: 17:
    :cvar POWER_DC: 1:8
    :cvar VOLTAGE_DC: 19
    :cvar CURRENT_DC: 20:
    :cvar SUNSP_INV_IMM_CTRL: 21:
    :cvar SUNSP_INV_OP_STATE: 22:
    :cvar SUNSP_INV_MODEL: 23:
    :cvar PH24: 24:
    :cvar PH25: 25:
    :cvar PH26: 26:
    :cvar PH27: 27:
    :cvar PH28: 28:
    :cvar PH29: 29:
    :cvar BI_DIR_FLEX_MGMT: 30:
    :cvar UNI_DIR_FLEX_LOAD_MGMT: 31:
    :cvar UNI_DIR_FLEX_FEED_IN_MGMT: 32:
    :cvar CURTAILMENT: 33:
    :cvar PH34: 34:
    :cvar PH35: 35:
    :cvar PH36: 36:
    :cvar PH37: 37:
    :cvar PH38: 38:
    :cvar POWER_MONITOR: 39:
    :cvar ENERGY_MONITOR: 40:
    :cvar DYNAMIC_CTRL: 41:
    :cvar HEAT_PUMP_BASE: 42:
    :cvar HEAT_COOL_CTRL: 43:
    :cvar POWER_CTRL: 44:
    :cvar DOM_HOT_WATER_CTRL: 45:
    :cvar BUFFER_STORAGE_CTRL: 46:
    :cvar ROOM_TEMP_CTRL: 47:
    :cvar PH48: 48:
    :cvar PH49: 49:
    :cvar ROOM_TEMP: 50:
    :cvar OUTSIDE_AIR_TEMP: 51:
    :cvar WATER_TEMP: 52:
    :cvar DEVICE_TEMP: 53:
    :cvar PROCESS_TEMP: 54:
    :cvar PH55: 55:
    :cvar PH56: 56:
    :cvar PH57: 57:
    :cvar PH58: 58:
    :cvar PH59: 59:
    :cvar SG_READY_STATES_BWP: 60:
    :cvar SGR_STATES_EVSE: 61:
    :cvar EEGCURTAILMENT: 62:
    :cvar PH63: 63:
    :cvar PH64: 64:
    :cvar PH65: 65:
    :cvar PH66: 66:
    :cvar PH67: 67:
    :cvar PH68: 68:
    :cvar PH69: 69:
    :cvar BI_DIR_CHARGING: 70:
    :cvar EVSESTATE: 71:
    :cvar EVSTATE: 72:
    :cvar PH73: 73:
    :cvar PH74: 74:
    :cvar PH75: 75:
    :cvar PH76: 76:
    :cvar PH77: 66:
    :cvar PH78: 78:
    :cvar PH79: 79:
    """
    UNDEF = "UNDEF"
    ACTIVE_ENERGY_AC = "ActiveEnergyAC"
    REACTIVE_ENERGY_AC = "ReactiveEnergyAC"
    APPARENT_ENERGY_AC = "ApparentEnergyAC"
    ACTIVE_POWER_AC = "ActivePowerAC"
    REACTIVE_POWER_AC = "ReactivePowerAC"
    APPARENT_POWER_AC = "ApparentPowerAC"
    VOLTAGE_AC = "VoltageAC"
    CURRENT_AC = "CurrentAC"
    POWER_FACTOR = "PowerFactor"
    PHASE_ANGLE = "PhaseAngle"
    CURRENT_QUADRANT = "CurrentQuadrant"
    FREQUENCY = "Frequency"
    ACTIVE_ENER_BALANCE_AC = "ActiveEnerBalanceAC"
    REACTIVE_ENER_BALANCE_AC = "ReactiveEnerBalanceAC"
    CURRENT_DIRECTION = "CurrentDirection"
    POWER_QUADRANT = "PowerQuadrant"
    ENERGY_DC = "EnergyDC"
    POWER_DC = "PowerDC"
    VOLTAGE_DC = "VoltageDC"
    CURRENT_DC = "CurrentDC"
    SUNSP_INV_IMM_CTRL = "SunspInvImmCtrl"
    SUNSP_INV_OP_STATE = "SunspInvOpState"
    SUNSP_INV_MODEL = "SunspInvModel"
    PH24 = "ph24"
    PH25 = "ph25"
    PH26 = "ph26"
    PH27 = "ph27"
    PH28 = "ph28"
    PH29 = "ph29"
    BI_DIR_FLEX_MGMT = "BiDirFlexMgmt"
    UNI_DIR_FLEX_LOAD_MGMT = "UniDirFlexLoadMgmt"
    UNI_DIR_FLEX_FEED_IN_MGMT = "UniDirFlexFeedInMgmt"
    CURTAILMENT = "Curtailment"
    PH34 = "ph34"
    PH35 = "ph35"
    PH36 = "ph36"
    PH37 = "ph37"
    PH38 = "ph38"
    POWER_MONITOR = "PowerMonitor"
    ENERGY_MONITOR = "EnergyMonitor"
    DYNAMIC_CTRL = "DynamicCtrl"
    HEAT_PUMP_BASE = "HeatPumpBase"
    HEAT_COOL_CTRL = "HeatCoolCtrl"
    POWER_CTRL = "PowerCtrl"
    DOM_HOT_WATER_CTRL = "DomHotWaterCtrl"
    BUFFER_STORAGE_CTRL = "BufferStorageCtrl"
    ROOM_TEMP_CTRL = "RoomTempCtrl"
    PH48 = "ph48"
    PH49 = "ph49"
    ROOM_TEMP = "RoomTemp"
    OUTSIDE_AIR_TEMP = "OutsideAirTemp"
    WATER_TEMP = "WaterTemp"
    DEVICE_TEMP = "DeviceTemp"
    PROCESS_TEMP = "ProcessTemp"
    PH55 = "ph55"
    PH56 = "ph56"
    PH57 = "ph57"
    PH58 = "ph58"
    PH59 = "ph59"
    SG_READY_STATES_BWP = "SG-ReadyStates_bwp"
    SGR_STATES_EVSE = "SGrStates_EVSE"
    EEGCURTAILMENT = "EEGCurtailment"
    PH63 = "ph63"
    PH64 = "ph64"
    PH65 = "ph65"
    PH66 = "ph66"
    PH67 = "ph67"
    PH68 = "ph68"
    PH69 = "ph69"
    BI_DIR_CHARGING = "BiDirCharging"
    EVSESTATE = "EVSEState"
    EVSTATE = "EVState"
    PH73 = "ph73"
    PH74 = "ph74"
    PH75 = "ph75"
    PH76 = "ph76"
    PH77 = "ph77"
    PH78 = "ph78"
    PH79 = "ph79"


@dataclass
class SgrProfilenumberType:
    """Specification of design source 0 means: specified by SmartGridready, the
    Porfilenumber follows the SmargGirdready scheme.

    &gt;0 means: specfied by manufacturer hhhh, the Profilenumber
    followos a manufacturors scheme

    :ivar specs_owner_id: This number idntifies the creator of this
        instance definition 0 means "This is a SmartGridready
        specification, SGr definition are valid" means "designed and
        manufaturer hhhh" and a seperate set of definitions created by
        the manufacturer is valid The profile number
        hhhh.nnnn.uuuu.ss.VV.vv is documented in the SGr profile
        specification number
    :ivar profile_identification: The Profile Identfication identiofis
        the main profile classes. The enumeration text is also
        documented with numbers being referenced in the profile number
        hhhh.nnnn.uuuu.ss.VV.vv as nnnn
    :ivar sub_profile_ident:
    :ivar sgr_level_of_operation: SGrLevelOfOperation defines a controls
        complexity level 1) single contact 2) 2 or more contacts /state
        controlled interface 3) statical defined characteristics tables
        4) dynamic realtime control combined with statical defined
        characteristics tables 5) dynamic realtime control combined with
        dynamic changeable characteristics tables 6) prognosis based
        systems
    :ivar version_number:
    """
    class Meta:
        name = "SGrProfilenumberType"

    specs_owner_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "specsOwnerId",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    profile_identification: Optional[ProfileTypeEnumType] = field(
        default=None,
        metadata={
            "name": "profileIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    sub_profile_ident: Optional[SubProfileTypeEnumType] = field(
        default=None,
        metadata={
            "name": "subProfileIdent",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    sgr_level_of_operation: Optional[int] = field(
        default=None,
        metadata={
            "name": "sgrLevelOfOperation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    version_number: Optional[SgrVersionNumberType] = field(
        default=None,
        metadata={
            "name": "versionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SgrProfileDescriptionType:
    """
    Profile Element for to be used for the generation of SGrGenericDevices and
    the Ecore modelling the generation of the generic profile level interface
    class Profil Element zur Integration in generische Gerätedefinitionen oder
    zur Erzeugung von ecore-Modellierungen.

    :ivar profile_number:
    :ivar fp_name_list:
    :ivar fp_legib_desc: this is the published information related to
        this functional profile
    :ivar fp_prg_desc:
    :ivar profile_name:
    :ivar mro_visibility_indicator:
    """
    class Meta:
        name = "SGrProfileDescriptionType"

    profile_number: Optional[SgrProfilenumberType] = field(
        default=None,
        metadata={
            "name": "profileNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    fp_name_list: Optional[SgrNamelistType] = field(
        default=None,
        metadata={
            "name": "fpNameList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    fp_legib_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "fpLegibDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    fp_prg_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "fpPrgDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    profile_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "profileName",
            "type": "Attribute",
        }
    )
    mro_visibility_indicator: Optional[SgrMropresenceLevelIndicationType] = field(
        default=None,
        metadata={
            "name": "mroVisibilityIndicator",
            "type": "Attribute",
        }
    )
