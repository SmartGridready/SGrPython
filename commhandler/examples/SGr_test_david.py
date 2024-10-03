# Smartgrid Ready Libraries
from sgr_commhandler.modbus_interface import SgrModbusInterface


if __name__ == "__main__":

    # Create interface instance
    interface_file = 'SGr_HeatPump_Test.xml'
    sgr_component = SgrModbusInterface(interface_file)

    # OLD Read Value Method with functional_profile_name and datapoint_name as parameters 
    value = sgr_component.getval('HeatPumpBase', 'HPOpState')
    print(value)

    # NEW Read Value Method with datapoint.
    # First find the datapoint and then get the values from the datapoint object found.
    data_point = sgr_component.find_dp('HeatPumpBase', 'HPOpState')
    value = sgr_component.getval(data_point)
    print(value)

    # We can also search for more info in the datapoint, for example:
    register = sgr_component.get_register_type(data_point)
    multiplicator = sgr_component.get_multiplicator(data_point)
    unit = sgr_component.get_unit(data_point)
    power_10 = sgr_component.get_power_10(data_point)

    # Setval is only implemented in the old style, with functional_profile_name and datapoint_name
    "sgr_component.setval('ActiveEnerBalanceAC', 'ActiveImportAC', 10)"