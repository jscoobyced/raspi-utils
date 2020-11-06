import smbus
import time
import sys
from ina219 import INA219

class PowerFormatting:
    FULL    = 0x01
    SHORT   = 0x02
    PERCENT = 0x03
    CURRENT = 0x04

def read(ina219, parameter):

    voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
    shunt_voltage = ina219.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
    current = ina219.getCurrent_mA()                   # current in mA
    power = ina219.getPower_W()                        # power in W
    percent = (voltage - 6)/2.4*100
    if(percent > 100):percent = 100
    if(percent < 0):percent = 0
    result = ""
    if(PowerFormatting.FULL == parameter):
        result = printlong(voltage, current, power, percent)
    elif(PowerFormatting.SHORT == parameter):
        result = printshort(voltage, current, power, percent)
    elif(PowerFormatting.PERCENT == parameter):
        result = "{0}".format(int(percent))
    elif(PowerFormatting.CURRENT == parameter):
        result = "{0}".format(int(current))
    return result

def printlong(voltage, current, power, percent):
    discharge = ""
    if(current < 0):
        discharge = "dis"
    print("Load Voltage:\t\t{:6.3f} V".format(voltage))
    print("Battery {0}charging\t{1:9.6f} A".format(discharge, current/1000))
    print("Power:\t\t\t{:6.3f} W".format(power))
    print("Percent:\t\t{:3.1f}%".format(percent))
    return ""

def printshort(voltage, current, power, percent):
    return "{0},{1},{2:1.3f},{3}".format(int(voltage*100), int(current), power, int(percent))

if __name__=='__main__':
    ina219 = INA219(addr=0x42)
    read(ina219, 0)
    time.sleep(2)
    if(len(sys.argv) > 1):
        result = ""
        if(sys.argv[1] == "percent"):
            result = read(ina219, PowerFormatting.PERCENT)
        elif(sys.argv[1] == "current"):
            result = read(ina219, PowerFormatting.CURRENT)
        else:
            result = read(ina219, PowerFormatting.SHORT)
        print(result)
    else:
        read(ina219, PowerFormatting.FULL)
