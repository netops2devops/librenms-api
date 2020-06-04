import requests
from pprint import pprint
import json
import urllib3
urllib3.disable_warnings()

__version__ = "1.0"

class Connect:
    """
    Python client for LibreNMS REST API
    Endpoints documented under : https://docs.librenms.org/API/
    """

    def __init__(self, server, auth_token, verify=False, debug=0):
        
        self.server = server
        self.auth_token = auth_token
        self.base_url = server + '/api/v0'
        self.version = __version__
        self.headers = {
            'X-Auth-Token' : self.auth_token,
            'Content-Type' : "application/json"
            } 


    def get_device(self, device_name):
        """
        GET information for a specific device in librenms
        Returns extracted info in JSON format
        """

        url = self.base_url + '/devices/' + device_name 
        response = requests.get(url, headers = self.headers, verify=False).json()

        return response
   

    def del_device(self, device_name):
        """
        DELETE a device from LibreNMS
        Returns 'status': 'ok' if operation was a success!
        """

        url = self.base_url + '/devices/' + device_name

        try:

            response = requests.delete(url, headers = self.headers, verify=False).json()
            return response
      
        except Exception as e:
            print("#- The following ERROR occured -#")
            print(e)
            return response


    def add_device(self, device_name, snmp_version, snmp_community):
        """
        Discover and ADD a new device to LibreNMS
        Returns 'status': 'ok' when operation is a success
        """
        
        url = self.base_url + '/devices'
        info = { 
                 'hostname' : device_name, 'version' : snmp_version,
                 'community' : snmp_community
                }

        data = json.dumps(info)
        
        try:
            response = requests.post(url, headers = self.headers, data=data, verify=False).json()
            return response

        except Exception as e :
            print("ERROR occured while adding device {0}".format(device_name))
            return response


    def list_devices(self):
        """
        List info on all devices in LibreNMS
        Dumps JSON formatted data
        """

        url = self.base_url + '/devices'

        try:
            response = requests.get(url, headers = self.headers, verify=False).json()
            return response

        except Exception as e:
            print("The following ERROR encountered while getting device list")
            print(e)
            return response


    def discover_device(self, device_name):
        """
        Triggers SNMP discovery of a given device
        """

        url = self.base_url + '/devices/' + device_name + '/discover'

        try:
            response = requests.get(url, headers = self.headers, verify=False).json()
            return response

        except Exception as e:
            print("The following error occured while re-discovering the device {0}".format(device_name))
            print(e)
            return response
