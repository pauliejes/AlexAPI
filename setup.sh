#! /bin/bash
baselocation=$PWD
apt-get update
apt-get -y install libasound2-dev memcached python-pip mpg123 python-alsaaudio python-aubio
pip install -r requirements.txt
apt-get -y install python-dev python-pip gcc # Editions added by Raspberry Pi Guy to work with SenseHAT
pip install evdev
#cp initd_alexa.sh /etc/init.d/alexa #This part of the script did attempt to run Alexa on startup
#cd /etc/rc5.d                       #Undesired for my tutorial - but if you want to run Alexa on boot then feel free to change!
#ln -s ../init.d/alexa S99alexa
#touch /var/log/alexa.log
cd $baselocation
echo "Enter your ProductID:"
read productid
echo ProductID = \"$productid\" >> creds.py

echo "Enter your Security Profile Description:"
read spd
echo Security_Profile_Description = \"$spd\" >> creds.py

echo "Enter your Security Profile ID:"
read spid
echo Security_Profile_ID = \"$spid\" >> creds.py

echo "Enter your Security Client ID:"
read cid
echo Client_ID = \"$cid\" >> creds.py

echo "Enter your Security Client Secret:"
read secret
echo Client_Secret = \"$secret\" >> creds.py

ip=$(ifconfig eth0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)
echo "Open http://$ip:5000"
python ./auth_web.py 

amixer cset numid=3 1 # This sets the audio to the 3.5mm audio jack, Alexa will talk to any 3.5mm speaker. If you want Alexa to talk over HDMI then change the number 1 to a 2 here.
