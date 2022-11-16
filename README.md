# INDEX

1) How to use
2) Pip installation for developers
3) Directory structure

## 1) How to use

- getval(<fp_name>, <dp_name>) from **generic_interface.py** module (Implemented in restapi and modbus)
- setval(<fp_name>, <dp_name>, <value>) from **generic_interface.py** module (Only implemented for modbus)
	
generic_interface.py has a script with an example on how to use these functions.

- For the xsdata documentation and the library documentation please go to sgr_library folder in this directory. There you will find the specific the documentation.
- For EXAMPLES on how to use the library, you will also find them in the sgr_library file, as 'examples'.

## 2) Pip Instalation

### Pip Install from local repository (developer).
0) Create virtual enviroment:

		py -m venv venv
		venv\Scripts\activate
    
 1) Then we locally install over it our virtual enviroment:
Pip install -e is extremely useful when simultaneously developing a product and a dependency. The e flag makes our installed package editable. The setup.py file will install it locally as a package.


    	pip install -e C:\path\to\file\
	
	EXAMPLE: pip install -e C:\Users\admin\Desktop\SGrPython   


### DEPRECATED Pip Install from pypi testing server (user).

I uploaded the library as "sgr-demo-v0.0.4" for now.
You can download it with the following command.

    pip install --index-url https://test.pypi.org/simple/ sgr-demo-v0.0.4
    
    
## 3) Directory

- sgr_library: Is the folder which will be installed with the pip install command. In there 

- xml_files: Contains sample xml files for users to modify or use as example.

- xsd_files: Contains the SGr xsd files structure, from which the dataclasses in "sgr_library" directory were generated. 
You don't have to do this, since the classes come included in the pip install, but in case you want to change something, you can generate classes with the following command:

		xsdata --package data_classes xsd_files/SGrIncluder.xsd
	
- setup.py: The script that is executed when installing the library with pip.

	
- requirements.txt: required libraries are included in the setup of the file, but in case these fail, install from requierements.txt file.
	
		pip install -r requirements.txt
