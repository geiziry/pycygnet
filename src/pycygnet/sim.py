from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a data store with a holding register
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [20] * 4000) , # Initialize 100 holding registers starting at address 0
    ir=ModbusSequentialDataBlock(250, [10] * 10) , # Initialize 100 holding registers starting at address 0
)


context = ModbusServerContext(slaves={2:store}, single=False)

# initialize the server information
identity = ModbusDeviceIdentification()
identity.VendorName = 'APMonitor'
identity.ProductCode = 'APM'
identity.VendorUrl = 'https://apmonitor.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'Modbus Server'
identity.MajorMinorRevision = '3.0.2'

# Start the Modbus server
if __name__ == "__main__":
    # TCP Server
    StartTcpServer(
        context=context,
        host='localhost',
        identity=identity,
        address=('localhost', 502),
        # address=('172.17.113.21', 502),

    )

# %%
import win32com.client


# UpdateUISCommandComponent to update uiscommand component with the target datagroup to be active
uis_client = win32com.client.Dispatch("CxUis.UisClient")
uis_client.Connect("[5420]CENTRAL.UIS")
# uis_client.SendUISCommand("WL_MN_02_CTL_RD","DG_T_DEV",'DataType=i2;DGORD=0;DGTYPE=SnglRegRw;RegNum=2;Value=5',"")
uis_client.SendUISCommand("WL_MN_02_CTL_RD","TEST","","")
# %%
dds_client = win32com.client.Dispatch("CxDds.DdsClient")
dds_client.Connect("[5420]CENTRAL.DDS")

for device_id in dds_client.GetDeviceIdsByCategory("RD"):
    out=dds_client.GetDeviceProperty(device_id,'DevCommId')
    if out[1] == 'WL_MN_02_GW_CD':
        print(device_id)
    # print(out[1])
