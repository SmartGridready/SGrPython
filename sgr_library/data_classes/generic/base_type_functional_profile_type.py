from enum import Enum

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class FunctionalProfileType(Enum):
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
    :cvar ACTIVE_ENERGY_BALANCE_AC: 13:
    :cvar REACTIVE_ENERGY_BALANCE_AC: 14:
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
    :cvar SUNSP_COMMON001: 80 Sunspec: All SunSpec compliant devices
        must include this as the first model
    :cvar SUNSP_INVERTER101: 81 Sunspec: model for single phase inverter
        monitoring (Int and SF)
    :cvar SUNSP_INVERTER102: 82 Sunspec: model for split phase inverter
        monitoring (Int and SF)
    :cvar SUNSP_INVERTER103: 83 Sunspec: model for 3 phase inverter
        monitoring (Int and SF)
    :cvar SUNSP_INVERTER111: 84 Sunspec: model for single phase inverter
        monitoring using float values
    :cvar SUNSP_INVERTER112: 85 Sunspec: model for split phase inverter
        monitoring using float values
    :cvar SUNSP_INVERTER113: 86 Sunspec: model for s3 phase inverter
        monitoring using float values
    :cvar SUNSP_NAMEPLATE120: 87 Sunspec: Inverter Controls Nameplate
        Ratings
    :cvar SUNSP_BASIC_SETTINGS121: 88 Sunspec: Inverter Controls Basic
        Settings
    :cvar SUNSP_MEASUREMENT_STATUS122: 89 Sunspec: Inverter Controls
        Extended Measurements and Status
    :cvar SUNSP_IMM_CONTROL123: 90 Sunspec: Immediate Inverter Controls
    :cvar SUNSP_BASIC_STORAGE124: 91 Sunspec: SunspBasicStorage124
    :cvar SUNSP_MULT_MPP160: 92 Sunspec: Model for multiple Maximum
        Power Point Trackers
    :cvar SUNSP_STATIC_VOLT_VAR126: 93 Sunspec: Static Volt-VAR Arrays
        for Q = f (U/Uref)
    :cvar SUNSP_FREQ_WATT_PARAM127: 94 Sunspec: Parameterized Frequency-
        Watt compensation
    :cvar SUNSP_WATT_PF131: 95 Sunspec: Parameterized Watt-Power Factor
        Crv PF = f (P/Pmax)
    :cvar SUNSP_VOLT_WATT132: 96 Sunspec: Parameterized Voltage-Power
        Factor Crv P = f (U/Uref)
    :cvar SUNSP_FREQ_WATT_CRV134: 97 Sunspec: Curve-Based Frequency-Watt
        curve P = f (F/Fref)
    :cvar SUNSP_BATTERY_BASE_MODEL802: 98 Sunspec: Battery SOC
        management
    """
    UNDEF = "UNDEF"
    METERING = "Metering"
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
    ACTIVE_ENERGY_BALANCE_AC = "ActiveEnergyBalanceAC"
    REACTIVE_ENERGY_BALANCE_AC = "ReactiveEnergyBalanceAC"
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
    SUNSP_COMMON001 = "SunspCommon001"
    SUNSP_INVERTER101 = "SunspInverter101"
    SUNSP_INVERTER102 = "SunspInverter102"
    SUNSP_INVERTER103 = "SunspInverter103"
    SUNSP_INVERTER111 = "SunspInverter111"
    SUNSP_INVERTER112 = "SunspInverter112"
    SUNSP_INVERTER113 = "SunspInverter113"
    SUNSP_NAMEPLATE120 = "SunspNameplate120"
    SUNSP_BASIC_SETTINGS121 = "SunspBasicSettings121"
    SUNSP_MEASUREMENT_STATUS122 = "SunspMeasurementStatus122"
    SUNSP_IMM_CONTROL123 = "SunspImmControl123"
    SUNSP_BASIC_STORAGE124 = "SunspBasicStorage124"
    SUNSP_MULT_MPP160 = "SunspMultMPP160"
    SUNSP_STATIC_VOLT_VAR126 = "SunspStaticVoltVar126"
    SUNSP_FREQ_WATT_PARAM127 = "SunspFreqWattParam127"
    SUNSP_WATT_PF131 = "SunspWattPF131"
    SUNSP_VOLT_WATT132 = "SunspVoltWatt132"
    SUNSP_FREQ_WATT_CRV134 = "SunspFreqWattCrv134"
    SUNSP_BATTERY_BASE_MODEL802 = "SunspBatteryBaseModel802"