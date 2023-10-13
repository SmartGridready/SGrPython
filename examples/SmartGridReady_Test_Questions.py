# add SmartGridReady libraries
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

# Import generated Data Classes
from sgr_library.data_classes.ei_rest_api import SgrRestapideviceDescriptionType
from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType

# Smartgrid Ready Libraries
from sgr_library.OLD_restapi_interface import RestapiInterface
from sgr_library.modbus_interface import SgrModbusInterface, find_dp

# os and configparser
import configparser
import os


class smartgridready_component():
    # class for component with smartgridready compatibility

    def __init__(self, bus_type:str, XML_file:str):
        # set XML file with external interface description - OLD MECHANISM   
        #self.interface_file = XML_file
        #self.interface_file_path_default = os.path.join(os.path.dirname(os.path.realpath(__file__)),  self.interface_file)
        
        # instanciate an XML parser - OLD MECHANISM
        #self.Parser = Parser(self.interface_file_path_default) 
        #self.address = self.Parser.address_return()             # get Modbus address and port
        #self.port = self.Parser.port_return()

        # instanciate an external interface (EI) to connect with the device - OLD MECHANISM
        #if bus_type == 'modbus':
        #    self.EI = EI4Modbus(self.port, self.address, self.interface_file)
        #else:    
        #    self.EI = None                  # --- add additional interfaces here
        
        # read configuration and interface files - NEW MECHANISM
        config_file_path_default = os.path.join( os.path.dirname(os.path.realpath(__file__)), config_file)
        config_ressource = configparser.ConfigParser()
        config_ressource.read(config_file_path_default)
        
        interface_file = XML_file
        parser = XmlParser(context=XmlContext())
        if bus_type == 'modbus':
            self.root = parser.parse(interface_file, SgrModbusDeviceDescriptionType)   # ADDED # NOT NEEDED
            self.sgr_reader_interface = SGrModbusInterface(interface_file) # ADDED
        elif bus_type == 'rest_api':
            self.root = parser.parse(interface_file, SgrRestapideviceDescriptionType)
            self.sgr_reader_interface = RestapiInterface(interface_file, config_ressource)
        else:
            self.root = None
            self.sgr_reader_interface = None     

    def read_value(self, functional_profile: str, data_point: str):
        # read one value from a given data point within a functional profile
        
        value = 0
        unit = None
        error_code = 100         # not found

        """fp_profiles = self.Parser.fp_return()   # get all functional profiles in XML file - OLD MECHANISM
        fp_profiles = self.root.fp_list_element # get all functional profiles in XML file - NEW MECHANISM
        for fp in fp_profiles:
            if fp == functional_profile:
                for dp in fp_profiles[fp]:
                    if dp == data_point:
                        name = dp.data_point[0].datapoint_name                     # get name - NEW MECHANISM
                        #value = EI.value_decoder(int(fp_profiles[fp][dp]['addr']))  # get value - OLD MECHANISM
                        value = dp.data_point[0].datapoint_value                    # get value - NEW MECHANISM, IS SYNTAX CORRECT ???
                        #Datapoint attribute: dp.data_point[0].basic_data_type.float32  # get attribute - WHAT'S THE DIFFERENCE BETWEEN ATTRIBUTE AND VALUE?
                        #unit = fp_profiles[fp][dp]['unit']                         # get unit - OLD MECHANISM
                        unit = dp.data_point[0].datapoint_unit                      # get unit - NEW MECHANISM, IS SYNTAX CORRECT, DO UNITS EXIST ???
                        error_code = 0"""

        # This makes all the search for you and gets you the decoded value.
        value = self.sgr_reader_interface.get_val(functional_profile, data_point)
        # If you want unit and name you can use the datapoint_info function. This one has to be refactored,
        # so it is more intuitive for the user.
        # [0] for addres, [1] for size, [2] for bitrank, [3] for register_type, [4] for unit, [5] for multiplicator, [6] for power_off
        
        unit = self.sgr_reader_interface.datapoint_info[4]

        # The datapoint name I did not add yet to the datapoint_info function but you can manually find it doing this for example:

        dp = find_dp(self.root, functional_profile, data_point)
        name = dp.data_point[0].datapoint_name
        error_code = 0
        
        return [value, unit, error_code]
                
    def write_value(self, functional_profile:str, data_point:str, value:float):
        # write one value to a given data point within a functional profile

        self.sgr_reader_interface.setval(functional_profile, data_point, value)

        None    # --- code under contruction, EI4_ModbusTCP does not support writing yet ---
        error_code = 0

        return error_code