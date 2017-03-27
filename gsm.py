 #!/usr/bin/env python

import time
import serial

def sendRequest(url):
    ser.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+SAPBR=3,1,"APN","CMNET"\r')
    time.sleep(1)
    print ser.read(1000)
    #ser.write('AT+SAPBR=1,1\r')
    #time.sleep(5)
    #print ser.read(1000)
    ser.write('AT+HTTPINIT\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+HTTPPARA="url","%s"\r' % url)
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+HTTPACTION=0\r')
    time.sleep(20)
    print ser.read(1000)
    ser.write('AT+HTTPREAD\r')
    time.sleep(1)
    response = ser.readlines()[2].strip()
    ser.write('AT+HTTPTERM\r')
    time.sleep(1)
    print ser.read(1000)
    return response

def shouldUnlock():
    response = sendRequest('http://www.azhibo.com/block/controll')
    return response


ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

while True:
    ser.write('AT\r')
    time.sleep(1)
    output = ser.readlines()[1].strip()
    print output
    if output == 'OK':
        break
print sendRequest('http://www.azhibo.com/block/controll')
ser.close()


