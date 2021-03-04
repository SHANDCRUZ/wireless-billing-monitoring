# DRIVE DATA MONITORING

### STEPS

 * [IMPORTING NECESSARY LIBRARIES. ](#IMPORTING LIBRARY)
 * [INITIALIZING SERIAL MODBUS CLIENT INSTANCE(OBJECT). ](#INITIALIZING SERIAL MODBUS CLIENT INSTANCE(OBJECT))
 * [INITIALIZING CLIENT SERVER CONNECTION. ](#INITIALIZING CLIENT SERVER CONNECTION)
 * [CALCULATING ADDRESS FOR HOLDING REGISTER. ](#CALCULATING ADDRESS FOR HOLDING REGISTER)
 * [READING PARAMETER FROM DRIVE. ](#READING PARAMETER FROM DRIVE)
 * [SCALING THE PARAMETER VALUE. ](#SCALING THE PARAMETER VALUE)
 * [SENDING DATA TO THE DASHBOARD. ](#SENDING DATA TO THE DASHBOARD)
 * [ENTIRE IMPLEMENTATION. ](#ENTIRE IMPLEMENTATION)
 * [WRITING DATA INTO THE HOLDING REGISTER. ](#WRITING DATA INTO THE HOLDING REGISTER)
 * [ADDITONAL CASE - SIEMENS REQUIREMENTS. ](#PEAK TORQUE AND PEAK CURRENT REQUIREMENTS)

---
# IMPORTING LIBRARY

Importing the Necessary Library for establishing the serial communication between the drive(FC-302) and the desktop  
 
 
 #### Code

```yaml

import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Adafruit_IO import Client, Feed

```
---
