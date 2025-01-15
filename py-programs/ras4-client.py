from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.object import BinaryValueObject
from bacpypes.apdu import WritePropertyRequest, ConfirmedRequestSequence
from bacpypes.primitivedata import Boolean
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address
import time

# BACnet device configuration
device_info = {
    "objectIdentifier": ('device', 123),
    "objectName": "FireAlarmClientDevice",
    "maxApduLengthAccepted": 1024,
    "segmentationSupported": "segmentedBoth",
    "vendorIdentifier": 15
}

# Create the local device object
local_device = LocalDeviceObject(**device_info)

# Create BACnet application
app = BIPSimpleApplication(local_device, "172.16.17.104")  # Use the correct server IP address

# BACnet Binary Value (simulating the fire alarm)
fire_alarm = BinaryValueObject(
    objectIdentifier=('binaryValue', 1),
    objectName="FireAlarmStatus",
    presentValue=False,  # Initially inactive
)

server_address = Address("172.16.17.113")

# Send fire alarm status to the server
def send_fire_alarm_status(status):
    write_request = WritePropertyRequest(
        objectIdentifier=fire_alarm.objectIdentifier,
        propertyIdentifier="presentValue",
        propertyValue=Boolean(status),
    )

    write_request.pduDestination = server_address

    # Create an IOCB for the request
    iocb = IOCB(write_request)
    app.request(iocb)

    # Wait for the confirmation from the server
    iocb.wait()  # This will block until the server responds
    if iocb.ioResponse:
        print(f"Fire Alarm Status sent successfully: {status}")
    else:
        print("Failed to send Fire Alarm Status.")

# Run the client and send status updates
try:
    while True:
        send_fire_alarm_status(True)  # or False for inactive
        time.sleep(5)  # Change status every 5 seconds
except KeyboardInterrupt:
    print("Client stopped.")
