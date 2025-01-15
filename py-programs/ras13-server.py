from bacpypes.app import BIPSimpleApplication
from bacpypes.object import BinaryValueObject
from bacpypes.local.device import LocalDeviceObject
from bacpypes.apdu import ReadPropertyRequest, WritePropertyRequest
from bacpypes.primitivedata import Unsigned, Boolean
from bacpypes.constructeddata import ArrayOf
import time

device_info = {
   "objectName": "FireAlarmDevice",
   "objectIdentifier": 1234,
   "maxApduLengthAccepted": 1024,
   "segmentationSupported": "segmentedBoth",
   "vendorIdentifier": 15
}

local_device = LocalDeviceObject(**device_info)

app = BIPSimpleApplication(local_device, "172.16.17.113")
fire_alarm = BinaryValueObject(
    objectIdentifier=('binaryValue', 1),
    objectName="FireAlarmStatus",
    presentValue=False,  # Initially inactive
)

app.add_object(fire_alarm)

# Handle WritePropertyRequest from client
def handle_write_property_request(request):
    if isinstance(request, WritePropertyRequest):
        object_instance = request.propertyIdentifier
        # Check if it's the fire alarm object
        if object_instance == 'presentValue':
            new_value = request.propertyValue.value
            print(f"Received fire alarm status: {new_value}")
            fire_alarm.presentValue = new_value
            request.respond()

app.receive_handler = handle_write_property_request

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Server stopped")