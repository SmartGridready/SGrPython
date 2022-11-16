import http.client
import json
from jinja2 import Template
import jmespath
import base64
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext



def add_private_config(string, params):
    jT = Template(string)
    a = jT.render(params['AUTHENTICATION'])
    return a

class RestapiConnect():
    """
    SmartGrid ready External Interface Class for Rest API
    """
    def __init__(self, root, private_config):
        self.root = root
        self.restapi_resource = self.root.rest_apiinterface_desc.trsp_srv_rest_uriout_of_box
        restapi_auth_method = self.root.rest_apiinterface_desc.rest_apiauthentication_method.value

        # Bearer Auth
        if restapi_auth_method == 'BearerSecurityScheme':
            
            bearer = self.root.rest_apiinterface_desc.rest_apibearer
            endpoint = bearer.rest_apiend_point.split("'")
            auth_endpoint = endpoint[2][1:] # Regex?
            request = endpoint[1]
            json_data = add_private_config(request, private_config)
            print(json_data)
            restapi_JMES_path = bearer.rest_apijmespath
            self.conn = http.client.HTTPSConnection(self.restapi_resource, timeout=10)
            self.headers = {'Content-type': 'application/json',
                            'Accept': 'application/json'}
            #json_data = json.dumps(json.loads(auth_request))
            self.conn.request('POST', auth_endpoint, json_data, self.headers)
            response = self.conn.getresponse()
            response_dec = json.loads(response.read().decode())
            print(response_dec)
            print(token)
            token = jmespath.search(restapi_JMES_path, response_dec)
            self.headers['Authorization'] = 'Bearer ' + token

        #TODO Basic Auth !!! Need to have an xml file with this structure to do it properly.
        elif restapi_auth_method == 'BasicSecurityScheme':
            auth_location = self.root.rest_apiinterface_desc.rest_apiauthentication_method.rest_apibasic.rest_apibasic_location

            self.conn = http.client.HTTPSConnection(self.restapi_resource, timeout=10)
            # reads the user and pass, encode it and add it to the header
            u = private_config['AUTHENTICATION']['username']
            p = private_config['AUTHENTICATION']['password']
            s = u + ':' + p
            s_bytes = s.encode('ascii')
            b64_bytes = base64.b64encode(s_bytes)
            b64_string = b64_bytes.decode('ascii')

            self.headers = {'Content-type': 'application/json', 'Authorization': 'Basic ' + b64_string}
            
        else:
            print('Error')

    def get(self, end_point):
        """
        HTTP Get request
        """
        self.conn = http.client.HTTPSConnection(self.restapi_resource, timeout=10)
        self.conn.request('GET', end_point , '', self.headers)
        response = self.conn.getresponse()
        response_dec = json.loads(response.read().decode())
        return response_dec

    def post(self, end_point, body):
        self.conn = http.client.HTTPSConnection(self.restapi_resource, timeout=10)
    
        #TODO Test system in which we can give either a string or a dictionary.
        if type(body) == dict:
            body = json.dumps(body)
        elif type(body) == str:
            body = json.loads(body)
            body = json.dumps(body)

        self.conn.request('POST', end_point, body, self.headers)
        response = self.conn.getresponse()
        print(response.status, response.reason)

    def put(self, end_point, value_to_send):
        #TODO to implement
        pass

    def patch(self, end_point, value_to_send):
        #TODO to implement
        pass