#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

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
Direction = -1 # > 0 clockwise, < 0 counter clockwise

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)

Step = 0

# Start main loop
while True:

  print Step,
  print Seq[Step]

  if (Direction < 0):
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

  # Wait before moving on
  time.sleep(WaitTime)
