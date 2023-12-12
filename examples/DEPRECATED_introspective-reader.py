# Diese Python file basiert dem "smartGrid_Ready_python_restapi_alpha_read_energy_monitor.py" von Gino (Merci!!)

import logging
import threading
import time
import configparser
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

# Import generated Data Classes
from sgr_library.data_classes.ei_rest_api import SgrRestapideviceDescriptionType
from sgr_library.data_classes.ei_modbus import SgrModbusDeviceDescriptionType

# Smartgrid Ready Libraries
from sgr_library.OLD_restapi_interface import RestapiInterface


###################################################################################
# simple reader
###################################################################################
def Reader(sgr_interface, stop_reader):


    interface = sgr_interface
    logging.info("Reader: started")
    
    # Private_config and communication_channel can be deleted once we add this to the python library
    interface.get_val_detailed("ActivePowerAC", "ActivePowerACtot") 
    
    while not stop_reader.is_set():
        # Repeat loop every 4 sec
        time.sleep(2)
        
        cycle_start_timestamp = time.time()
        interface.cycle_start_timestamp = cycle_start_timestamp
        logging.info("Reader: cycle started at {}".format(time.ctime(cycle_start_timestamp)))
        # We loop inside the functional profiles and then into the datapoints
        for fp in root.fp_list_element:
            for dp in fp.dp_list_element:
                FP_Name = fp.functional_profile.profile_name
                DP_Name = dp.data_point[0].datapoint_name
                interface.get_val_detailed(FP_Name, DP_Name)
            
        time.sleep(2)

    logging.info("Reader: received stop_reader. Exiting")


###################################################################################
# Simulationsparameter
###################################################################################
simulation_duration = 17 #3  # stop the simulation after X seconds
config_file = 'config_CLEMAPEnMon_ressource_default.ini'
#interface_file = 'CLEMAP_ModbusMeterV0.1.1.xml'
interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'

###################################################################################
# Main Simulationsprogramm
###################################################################################
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig( format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # read configuration and interface files
    config_file_path_default = os.path.join( os.path.dirname(os.path.realpath(__file__)), config_file)
    config_ressource = configparser.ConfigParser()
    config_ressource.read(config_file_path_default)
    
    interface_file = 'SGr_04_0018_CLEMAP_EIcloudEnergyMonitorV0.2.1.xml'
    parser = XmlParser(context=XmlContext())
    root = parser.parse(interface_file, SgrRestapideviceDescriptionType)


    sgr_reader_interface = RestapiInterface(interface_file, config_ressource)


    # print interface
    print('***** SGr FP *****')
    print(f"device {root.device_name} of kind {root.device_profile.device_kind} by manufacturer {root.manufacturer_name}")

    for fp in root.fp_list_element:
        FP_Name = fp.functional_profile.profile_name
        for dp in fp.dp_list_element:
            DP_Name = dp.data_point[0].datapoint_name
            print(f' SGr DP {DP_Name}')
            print(f'    Datapoint Attribute: {dp.data_point[0].basic_data_type.float32}')
    print('*****')



    # loop through a number of iterations
    reader_stop_event = threading.Event()
    logging.info("Main: starting reader ...")

    reader_thread = threading.Thread(target = Reader, args =(sgr_reader_interface, reader_stop_event, ))
    reader_thread.start()

    simulation_start_timestamp = time.time()

    while time.time() - simulation_start_timestamp < simulation_duration:
        logging.info(".")
        time.sleep(1)

    logging.info("Main: stopping reader ...")
    reader_stop_event.set()
    time.sleep(2)
    logging.info("Main: Bye Bye!")
