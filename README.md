# DRIVE DATA MONITORING

### STEPS

* [IMPORTING NECESSARY LIBRARIES.](#IMPORTING_LIBRARY)
* [INITIALIZING SERIAL MODBUS CLIENT INSTANCE(OBJECT).](#INITIALIZING_SERIAL_MODBUS_CLIENT_INSTANCE(OBJECT))
* [INITIALIZING CLIENT SERVER CONNECTION. ](#INITIALIZING_CLIENT_SERVER_CONNECTION)
* [CALCULATING ADDRESS FOR HOLDING REGISTER. ](#CALCULATING_ADDRESS_FOR_HOLDING_REGISTER)
* [READING PARAMETER FROM DRIVE. ](#READING_PARAMETER_FROM_DRIVE)
* [SCALING THE PARAMETER VALUE. ](#SCALING_THE_PARAMETER_VALUE)
* [SENDING DATA TO THE DASHBOARD. ](#SENDING_DATA_TO_THE_DASHBOARD)
* [ENTIRE IMPLEMENTATION. ](#ENTIRE_IMPLEMENTATION)
* [WRITING DATA INTO THE HOLDING REGISTER. ](#WRITING_DATA_INTO_THE_HOLDING_REGISTER)
* [ADDITONAL CASE - SIEMENS REQUIREMENTS. ](#PEAK_TORQUE_AND_PEAK_CURRENT_REQUIREMENTS)



---
## IMPORTING_LIBRARY

Importing the Necessary Library for establishing the serial communication between the drive(FC-302) and the desktop  
 
 
 #### CODE

```yaml

import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Adafruit_IO import Client, Feed

```

---

## INITIALIZING_SERIAL_MODBUS_CLIENT_INSTANCE(OBJECT)

The Protocol used to communicated with the drive FC-302 is Modbus RTU protocol with the Default Baudrate of 192600.
The 8 byte of data is send to the drive to retrive the information and the parity is 'EVEN'



#### CODE

```yaml

client = ModbusClient(method = 'rtu', port='COM3', baudrate= 19200, bytesize =8, parity='E')
connection = client.connect()
print(connection)

```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| client   | Has the Modbus RTU client connection |  object of the connection class |  object |



---

## INITIALIZING_CLIENT_SERVER_CONNECTION

Here we are initializing the Client Server connection between the desktop and the dashboard.
We need to pass the key and username credentials to the aio client object.


#### CODE

```yaml

ADAFRUIT_IO_KEY = 'eea9210ecf3a46d5b7e7c3f67e4e8303'
ADAFRUIT_IO_USERNAME = 'SHAN_D_CRUZ'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

```

#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| aio   | Has client connection for dashboard |  object of the dashboard |  object |


---

## CALCULATING_ADDRESS_FOR_HOLDING_REGISTER

The parameter value such as current are stored in the Holding Register and to retrive the data from the drive, we need to pass the holding register address.
The value of holding register address is given by (parameter_index*10) -1


#### CODE

```yaml

parameter = {
    "power-in-kw": 1610,
    "voltage": 1612,
    "current": 1614,
    "torque": 1616,
    "speed": 1617        
    }
# The Paramater value are the value present in the FC-302 manual or from the LCP display or from VLT software
# Any register Address in the drive is given be 
# Holding Register address = (Parameter_number*10)-1 ------> converting to HEX value (not Mandatory)

def _getaddress(value):
    value = (value*10)-1
    return value

address = _getaddress(parameter[key])

```

#### Return Values

| Name          | Description | Type       |
| ------------- |-------------| ---------- |
| address   | Has address of holding register | int |


---

## READING_PARAMETER_FROM_DRIVE
Now reading the parameter value from the holding register.

#### CODE

```yaml
read = client.read_holding_registers(address=address, count=2, unit = 0x1)
read_data = read.registers
# ADDRESS -------> ADDRESS OF THE PARAMETER TO BE READ FOR THE DRIVE
# COUNT   -------> NUMBER OF BYTES TO BE READ FROM THAT ADDRESS
# UNIT    -------> THE SLAVE ADDRESS (USUALLY 0X1)

```

#### Return Values

| Name          | Description | Type       |
| ------------- |-------------| ---------- |
| read   | Has object of holding register | object |
| read_data| Has the value of the holding register | depend on parameter(int, float) |


---

## SCALING_THE_PARAMETER_VALUE
Now scaling the parameter value read from the drive.


#### CODE

```yaml

# The Actual output data from drive will not give the exact value.
# So scaling is important for the parameter.
doscaling = {
    "power-in-kw": 100,
    "current": 100,
    "voltage":10,
    "torque": 10    
    }
    
```


---

## SENDING_DATA_TO_THE_DASHBOARD
After the data has been retrived from the drive, it has to be sent to dashboard.


#### CODE

```yaml

aio.send_data(paramkey[key], data)
time.sleep(2)

```

---

## ENTIRE_IMPLEMENTATION
Actually the above steps are looped over for the parameter to be read and sending to dashboard


#### CODE

```yaml

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 11:44:27 2021

@author: Shanmugam M (@SHANDCRUZ)
"""
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#initialize a serial RTU client instance
from Adafruit_IO import Client, Feed

ADAFRUIT_IO_KEY = 'eea9210ecf3a46d5b7e7c3f67e4e8303'
ADAFRUIT_IO_USERNAME = 'SHAN_D_CRUZ'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
#feeddata = aio.feeds('drivedata')[1]
stopfeed = aio.feeds('stop')[1]
aio.send_data(stopfeed, 0)
stop = 0
#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from

client = ModbusClient(method = 'rtu', port='COM3', baudrate= 19200, bytesize =8, parity='E')

#Connect to the serial modbus server
connection = client.connect()
print(connection)

peakparam = ["peaktorque", "peakcurrent"]
peakparamkey = {}
Maxparam = {
    "torque": 0,
    "current": 0
    }

for i in peakparam:
    try:
        temp = aio.feeds(i)
        peakparamkey.update({i:temp[1]})
    except:
        new_feed = Feed(name=i)
        aio.create_feed(new_feed)
        temp = aio.feeds(i)
        peakparamkey.update({i:temp[1]})

def _getaddress(value):
    value = (value*10)-1
    return value

parameter = {
    "power-in-kw": 1610,
    "voltage": 1612,
    "current": 1614,
    "torque": 1616,
    "speed": 1617        
    }

paramkey = {}

doscaling = {
    "power-in-kw": 100,
    "current": 100,
    "voltage":10,
    "torque": 10    
    }



for key, value in parameter.items():
    try:
        temp = aio.feeds(key)
        paramkey.update({key:temp[1]})
    except:
        new_feed = Feed(name=peakparam)
        aio.create_feed(new_feed)
        temp = aio.feeds(peakparam)
        paramkey.update({key:temp[1]})

while(stop == 0):
    senddata ={}
    connection = client.connect()
    print(connection)
    for key,value in parameter.items():
        print(parameter[key])
        address = _getaddress(parameter[key])
        print("\nAddress is")
        print(address)
        # Read the parameter Listed.
        read = client.read_holding_registers(address=address, count=2, unit = 0x1)
        readdata = read.registers
        print(readdata, type(readdata),len(readdata))
        data = max(readdata)
        print(type(data))
        if key in doscaling:
            data = data/doscaling[key]
        
        tempkey = "peak"+key
        print(tempkey)
        if tempkey in peakparam:
            print("entered")
            if (Maxparam[key] < data):
                Maxparam[key] = data
                aio.send_data(tempkey, Maxparam[key])
                print("peak param send")
        datastr = str(data)
        print(key+"  :  "+datastr)
        senddata.update({key:data})
        print('\n')
        
        aio.send_data(paramkey[key], data)
        time.sleep(2)       
    
    #aio.send_data(feeddata, senddata)
    print("Data send to cloud successfully!")
    stop = int(aio.data(stopfeed)[0][3])
    print(stop, type(stop))
    #Closes the underlying socket connection
    client.close()
    time.sleep(2)
    
 ```
 
 ---
 
 ## WRITING_DATA_INTO_THE_HOLDING_REGISTER
 The next is writing a data to the drive. This is same as reading the data from the drive.
 
 
 #### CODE
 
 ```yaml
 
 # The same steps for writing the value into the holding register of drive
# The Address of the parameter should be calculated
# The Number of bytes that the parameter holds
# The Slave address which it is intended to
# Say example in speed parameter address = 16169 (= 1617*10-1) and value is 700 

client.write_registers(address=address, count=2, unit = 0x1)

```

---

## PEAK_TORQUE_AND_PEAK_CURRENT_REQUIREMENTS
The Siemens wanted a requirement that the there should be Dashboard which should monitor the Motor parameter 
such as Torque and Current and it should display the peak torque and current that the motor has gone 
since it had been bought.
