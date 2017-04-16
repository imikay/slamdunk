 #!/usr/bin/env python

import time
import serial
import RPi.GPIO as GPIO

def sendRequest(url):
    ser.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+SAPBR=3,1,"APN","CMNET"\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+SAPBR=1,1\r')
    time.sleep(2)
    print ser.read(1000)
    #ser.write('AT+HTTPTERM\r') # Terminate the previous unterminated connection if there's any
    ser.write('AT+HTTPINIT\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+HTTPPARA="url","%s"\r' % url)
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+HTTPACTION=0\r')
    time.sleep(1)
    print ser.read(1000)
    ser.write('AT+HTTPREAD\r')
    time.sleep(1)
    response = ser.readlines()
    ser.write('AT+HTTPTERM\r')
    time.sleep(1)
    print ser.read(1000)

    return response

def start_count():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(36, GPIO.IN)

    count = 0

    start_time = time.time()
    print "New game starting ..."
    while (time.time() - start_time) < 60 :
          i=GPIO.input(36)

          if i == 1:
               count = count + 3
               print "Goal! Current score is ", count
          time.sleep(0.2)

    GPIO.cleanup(36)
    print "Time is up, your total score is ", count    
    return count

def gate_control(command):
    GPIO.setmode(GPIO.BOARD)

    # Define GPIO signals to use
    StepPins = [13,15,16,18]

    # Set all pins as output
    for pin in StepPins:
      print "Setup pins"
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)

    Seq = [[1,0],
           [1,1,],
           [0,1]]

    StepCount = len(Seq)

    # Read wait time from command line
    
    WaitTime = 1/float(1000)

    Step = 0

    now = time.time()
    # Start main loop
    while True:

      print Step,
      print Seq[Step]

      if (command < 0):
        GPIO.output(16, True)

      for pin in range(0, 2):
        xpin = StepPins[pin]
        if Seq[Step][pin]!=0:
          print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)

      Step += 1

      # If we reach the end of the sequence
      # start again
      if (Step>=StepCount):
        Step = 0

      if (time.time() - now) > 5:
        break
         
      # Wait before moving on
      time.sleep(WaitTime)

       
      
                                                   

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

while True:
    try:
        new_game = sendRequest('http://slamdunk.gousu.com')
        print new_game
        print new_game[2].strip()
        if new_game[2].strip() == '1':
            gate_control(1)
            count = start_count()
            gate_control(-1)
            sendRequest('http://slamdunk.gousu.com/play/end/%s' % count)
        else:
            print 'No one is playing'
        time.sleep(3)
    except KeyboardInterrupt:
        print "Exit \n"
    #except:
    #    print 'Connection failed'
    #finally:
    #    ser.close()


