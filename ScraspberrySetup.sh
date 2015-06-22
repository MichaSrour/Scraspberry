#!/bin/bash

#creating the service
mv scraspberry /etc/init.d/scraspberry
chmod 775 ScraspberryClient1.py
chmod 775 ScraspberryClient2.py
chmod 775 ScraspberryServer.py
chmod 775 Scraspberry.sh
chmod 775 /etc/init.d/scraspberry

#setting VERBOSE to yes in /lib/init/vars.sh
temp="yes" 
sed -i -e "s/\(VERBOSE=\).*/\1$temp/" /lib/init/vars.sh

#adding service to default run levels
update-rc.d scraspberry defaults

echo -e "\e[95mHurray! Scraspberry setup done! :)"
echo -e "\e[35mReboot your RaspberryPi"

