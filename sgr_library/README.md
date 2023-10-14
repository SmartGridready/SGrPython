# SGrLibrary and xsData "generation" and "parsing" instructions.

 1) Library use.

 2) xsdata branch (how to install and use).
 	- generation of classes from xsd
 	- xml parsing

 3) Directory structure.
 
# 1) Library use

- getval(<fp_name_string>, <dp_name_string>) from **generic_interface.py** module (Implemented in restapi and modbus)
- setval(<fp_nam_stringe>, <dp_name_string>, <value_integer>) from **generic_interface.py** module (Only implemented for modbus)

# 2) xsData documentation

## Introduction
In this branch we parse the xml file with the xsdata library. This library creates generated metadata classes from which you can navigate the xml file.

The advantage of this is that you can navigate the xml file directly on those classes, it is cleaner and more intuitive. 
You can also use the classes directly wihtout having to do create parser with lots of loops like you do with the ElementTree library.

The code looks cleaner and is easier to handle. The disadvantage is that you have to generate the classes from an xsdf file with an xsdata script, but we can maybe provide that xsd file and the generated classes to our clients so they don't have to do this.

## xsdata instalation and generation of classes
0) Create virtual enviroment:

		py -m venv venv
		venv\Scripts\activate
1) install library: 

		"pip install xsdata"
2) run script: 

		"xsdata --package <file_name> <xsd_file_name>"
	Keep the xsd file in the same directory.
	file_name will be the name of the folder with the generated classes.
	
## xsData Library xml parsing
1) We import the library and the generated classes:

		from  xsdata.formats.dataclass.parsers  import  XmlParser 
		from  xsdata.formats.dataclass.context  import  XmlContext
		from sgr_library.data_classes.product import DeviceFrame

3) We create a root element with xsdata parser: (lines 19 and 20 in smartGridReadyPythonLibrary_xsdata.py)

You can use the generated classes I created, they are in the data_info directory in the test.py file.

	parser = XmlParser(context=XmlContext())
	root = parser.parse(interface_file_path_default, DeviceFrame)

# 3) Directory documentation


## Files used in derectory

- **generic_interface.py**
	"this is from where we use our getval and setval functions"
	"abstraction layer of interface"

- modbus_client.py
	"Creates client to connect with the modbus server".
	
- modbus_interface.py
	"Contains get_val and set_val functions".
	
	"At the end of the file there is an example for the get_vale function usage"

- restapi_client.py
	"Makes connection with the api, also works with xsdata".

- restapi_iterface.py 

	"At the end of the file there is an example for the get_vale function usage"

	"New library with xsdata, it has two important functions:
	1) new_packet: makes a get request to the api to get a new json packet from the sensor.
	2) get_val: returns the value from a certain datapoint."



### Examples directory

- introspective-reader.py
"Has the format of the old reader we had in the library. I basically creates a loop and makes a getval over all the datapoints it finds in the xml file.
The only difference is that now it is implemented with xsdata library and does not need a parser".


