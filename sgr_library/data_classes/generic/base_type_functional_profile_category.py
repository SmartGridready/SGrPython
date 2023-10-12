from enum import Enum

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


class FunctionalProfileCategory(Enum):
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
