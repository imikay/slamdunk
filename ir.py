import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN)

count = 0;

try:
    while True:
              i = GPIO.input(36)                       
              print "Status: ", i

              if i == 1:                              
                   count = count + 3
                   print "Goal! Total score ", count
              time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
