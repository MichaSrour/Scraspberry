#!/bin/sh

/home/pi/Scraspberry/ScraspberryServer.py &
echo $! > /var/run/ServerPID.pid

/home/pi/Scraspberry/ScraspberryClient1.py &
echo $! > /var/run/ClientPID1.pid

/home/pi/Scraspberry/ScraspberryClient2.py &
echo $! > /var/run/ClientPID2.pid
