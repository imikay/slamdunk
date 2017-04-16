import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0;

try:
    while True:
              i=GPIO.input(12)                       

              if i == 0:                              
                   count = count + 3
                   print "Goal! Total score ", count
                   time.sleep(0.8)
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
