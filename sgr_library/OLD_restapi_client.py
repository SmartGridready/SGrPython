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

            service_call = self.root.rest_apiinterface_desc.rest_apibearer.service_call
            request_path = service_call.request_path #auth endpoint
            body = service_call.request_body #request
            query = service_call.response_query.query #accesToken

            
            #auth_endpoint = endpoint[2][1:] # Regex? #auth endpoint
            #request = endpoint[1] #body
            json_data = add_private_config(body, private_config)
            #restapi_JMES_path = bearer.rest_apijmespath #accesToken
            self.conn = http.client.HTTPSConnection(self.restapi_resource, timeout=10)
            self.headers = {'Content-type': 'application/json',
                            'Accept': 'application/json'}
            #json_data = json.dumps(json.loads(auth_request))
            self.conn.request('POST', request_path, json_data, self.headers)
            response = self.conn.getresponse()
            response_dec = json.loads(response.read().decode())

            token = jmespath.search(query, response_dec)
            self.headers['Authorization'] = 'Bearer ' + str(token)

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

        self.conn.request('POST', end_point, body=body, headers=self.headers)
        response = self.conn.getresponse()
        print(response.status, response.reason)

    def put(self, end_point, value_to_send):
        #TODO to implement
        pass

    def patch(self, end_point, value_to_send):
        #TODO to implement
        pass