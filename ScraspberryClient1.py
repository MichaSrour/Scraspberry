#! /usr/bin/python
import socket
import select
import string
import sys
import RPi.GPIO as GPIO
import time
from array import array
             
def sendCMD(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    s.send(a.tostring() + cmd)
##    print 'Sending Data'

##main function
if __name__ == "__main__":
     
    host = ''
    port = 42001
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
	
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
##    connect to remote host
    trying = 1
    while trying:
	try :
	    s.connect((host, port))
	    trying = 0
	except :
	    time.sleep(0.5)
#            sys.exit()
     
##    print 'Connected to remote host. Start sending messages'     
    running = 1
    while running:
        time.sleep(0.1)
        try:
            input_state = GPIO.input(31)
        except KeyboardInterrupt:
            running = 0
##        except Exception, e:
##            self.log(str(e))
        if input_state == False:
            time.sleep(0.2)
            out = 'broadcast "pin 31 off"'
            sendCMD(out)
        
      
