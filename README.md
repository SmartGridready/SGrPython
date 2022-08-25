

## Local pip instalation
0) Create virtual enviroment:

		py -m venv venv
		venv\Scripts\activate
    
 1) Then we locally install over it our virtual enviroment.
Pip install -e extremely useful when simultaneously developing a product and a dependency. The e flag makes our installed package editable. The setup.py file will install it locally as a package.


    pip install -e C:\path\to\file\ ![image](https://user-images.githubusercontent.com/26125579/186759475-b1c54cdf-8bea-4387-b778-910b9c5f4df6.png)


## pypi test server installation

I uploaded the library as sgr-demo-v0.0.4 for now

    pip install --index-url https://test.pypi.org/simple/ sgr-demo-v0.0.4
