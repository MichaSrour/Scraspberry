#! /usr/bin/python
import socket
import select
import RPi.GPIO as GPIO
import pdb
import sys
import struct
import time
from array import array
import os
          
 
##Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
##    Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
##                broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def processMessage(sock, message):
        if (message == 'broadcast kill'): running = 0
##        broadcasts = pinX output. X=number, output = on or off  
        temp=message.replace('\"','') 
        if temp[0:9] == 'broadcast':             
           messageParts = temp[10:].split()
           pinNumber = int(messageParts[1])
           if (pinNumber == 7)|(pinNumber == 11)|(pinNumber == 12)|(pinNumber == 13)|(pinNumber == 15)|(pinNumber == 16)|(pinNumber == 18)|(pinNumber == 22)|(pinNumber == 29):
               if (messageParts[2] == "on") | (messageParts[2] == "1"):
                    pinSetting = GPIO.HIGH
               else:
                    pinSetting = GPIO.LOW
               GPIO.output(pinNumber, pinSetting)
          
               
                
             
 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    ADDRESS_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 42001
    HOST = ''
    i=0
    j=0
    ip=''
    IP=''
    k=0
    l=0
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False) 
    GPIO.setup(7, GPIO.OUT) 
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(29, GPIO.OUT)
    
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    os.chdir("/home/pi/Scraspberry")
    f=open("ScraspberryLog.txt", 'w')
    f.close()

    try:
        server_socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST ,PORT))
        server_socket.listen(5)
        f=open("ScraspberryLog.txt", 'a')
        print "Socket Open & Scratch server started on port " + str(PORT) + '\n'
        f.write(time.ctime() + ' : Socket Open & Scratch server started on port' + str(PORT) + '\n')
        f.close()
        CONNECTION_LIST.append(server_socket)
        

    except socket.error, (value,message):
        if server_socket:
            server_socket.close()
        f=open("ScraspberryLog.txt", 'a')
        print "Could not open socket: " + message
        f.write(time.ctime() + ' : Could not open socket: ' + message + '\n')
        f.close()
        sys.exit(1)
        
    running = 1
    while running:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[], 0)
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                ADDRESS_LIST.append(addr)
                print "Client (%s, %s) connected" % addr
                f=open("ScraspberryLog.txt", 'a')
                f.write(time.ctime() + ' : Client (%s, %s) connected' % addr + '\n')
                f.close()
                           
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, data)
                        #print(data)

                        for i in range(0,len(CONNECTION_LIST)):
                            if CONNECTION_LIST[i]==sock:
                                j=i-1
                                ip=ADDRESS_LIST[j]
                            i=i+1
                        try:
                            pointer = 0
                            while pointer < len(data):
                                messageLength = struct.unpack(">l",data[pointer:pointer+4])[0]
                                thisMessage = data[pointer+4:pointer+4+messageLength]
                                pointer += messageLength + 4
                                processMessage(sock, thisMessage)
                                f=open("ScraspberryLog.txt", 'a')
                                f.write(time.ctime() + ' : Client %s sent: %s' % (ip, thisMessage) + '\n')
                                f.close()
                        except KeyboardInterrupt:
                            running = 0
                        except Exception, e:
                            self.log(str(e))

                except KeyboardInterrupt:
                    running = 0
                    
                except:
                    for k in range(0,len(CONNECTION_LIST)):
                        if CONNECTION_LIST[k]==sock:
                            l=k-1
                            IP=ADDRESS_LIST[l]
                        k=k+1    
                    broadcast_data(sock, "Client (%s, %s) is offline" % IP)
                    print "Client (%s, %s) is offline" % IP
                    f=open("ScraspberryLog.txt", 'a')
                    f.write(time.ctime() + ' : Client (%s, %s) offline' % IP + '\n')
                    f.close()
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    ADDRESS_LIST.remove(IP)
                    continue
                    
                    
        time.sleep(0.05)

    server_socket.close()
