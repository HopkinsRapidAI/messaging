import os
from pathlib import Path
import requests
import json
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv
import time

load_dotenv(Path(__file__).resolve().parent / ".env")
conn_str = os.environ["IOTHUB_CONNECTION_STR_GARAGE"]
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

coreurl =  "https://openapi.api.govee.com"
getDevicesurl = "/router/api/v1/user/devices"
getStateurl = "/router/api/v1/device/state"

headers = {
      "Content-Type":"application/json",
      "Govee-API-Key": os.environ["GOVEE_API_KEY"]
}


payload = {
    "requestId": "uuid",
    "payload": {
        "sku": "H5111",
        "device": "63:15:E1:3D:05:46:47:16"
    }
}

class iotrecorderStatefull:
    def __init__(self):
        self.data = []

    def record(self, data):
        self.data.append(data)

    def get_devices(self):
        return requests.get(coreurl+getDevicesurl, headers=headers)
    
    def get_deviceState(self, sku,device):
        payload = {
            "requestId":"uuid",
            "payload": {
                "sku": sku,
                "device": device
            }
        }
        payloadJson = json.dumps(payload)
        return requests.post(coreurl+getStateurl, headers=headers, data=payloadJson)

    def clear_data(self):
        self.data = []
        
if __name__ == "__main__":
    recorder = iotrecorderStatefull()
    response = recorder.get_devices()

    device_data = response.json()

    prettydevice = json.dumps(device_data, indent=4)
    #print(prettydevice)
    
    for i in range(1, 11):
        #print("\n\n ***** Getting Device State for *****\n\n")
        device_state = recorder.get_deviceState("H5111", "63:15:E1:3D:05:46:47:16")
        device_state_data = device_state.json()
        prettystate = json.dumps(device_state_data, indent=4)
        #print(prettystate)
        device_data = json.loads(prettystate)
        value = device_data["payload"]["capabilities"][1]["state"]["value"]
       
        message = Message( f'{{"messageIndex": "{i}", "temperature": {value}, "device":"Orin Garage Freezer"}}' )
        device_client.send_message(message)
        print(f"Message {i} sent! with value {value}")
        time.sleep(10)
  
 