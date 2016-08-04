# Alexa Personal Assistant Companion Program for Raspberry Pi
# Modified by Simon Beal and Matthew Timmons-Brown for "The Raspberry Pi Guy" YouTube channel
# Built upon the work of Sam Machin, (c)2016
# This is a library that includes all of the web functionality of the Alexa Amazon Echo personal assistant service
# The code here was originally in main.py, but has been abstracted for ease of use (you should not need to change it)

#! /usr/bin/env python

import os
import random
import time
import alsaaudio
import wave
import random
from creds import *
import requests
import json
import re
from memcache import Client

#Settings
device = "plughw:1" # Name of your microphone/soundcard in "arecord -L"
# Is your Amazon Echo clone not working? Perhaps the microphone is not connected properly or is not found at plughw:1
# Check and then modify this variable.

#Setup - details for Amazon server
recorded = False
servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))


# Check whether your Raspberry Pi is connected to the internet
def internet_on():
    print "Checking Internet Connection"
    try:
        r =requests.get('https://api.amazon.com/auth/o2/token')
	print "All systems GO"
        return True
    except:
	print "Connection Failed"
    	return False

# Sends access token to Amazon - value sent is unique to each device - we do not advise you to share it
def gettoken():
	token = mc.get("access_token")
	refresh = refresh_token
	if token:
		return token
	elif refresh:
		payload = {"client_id" : Client_ID, "client_secret" : Client_Secret, "refresh_token" : refresh, "grant_type" : "refresh_token", }
		url = "https://api.amazon.com/auth/o2/token"
		r = requests.post(url, data = payload)
		resp = json.loads(r.text)
		mc.set("access_token", resp['access_token'], 3570)
		return resp['access_token']
	else:
		return False
		
# Send the contents of "recording.wav" to Amazon's Alexa voice service
def alexa(sense):
	url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
	headers = {'Authorization' : 'Bearer %s' % gettoken()}
	d = {
   		"messageHeader": {
       		"deviceContext": [
           		{
               		"name": "playbackState",
               		"namespace": "AudioPlayer",
               		"payload": {
                   		"streamId": "",
        			   	"offsetInMilliseconds": "0",
                   		"playerActivity": "IDLE"
               		}
           		}
       		]
		},
   		"messageBody": {
       		"profile": "alexa-close-talk",
       		"locale": "en-us",
       		"format": "audio/S16; rate=16000; channels=1"
   		}
	}
	with open(path+'recording.wav') as inf:
		files = [
				('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
				('file', ('audio', inf, 'audio/S16; rate=16000; channels=1'))
				]	
		r = requests.post(url, headers=headers, files=files)
	if r.status_code == 200:
		for v in r.headers['content-type'].split(";"):
			if re.match('.*boundary.*', v):
				boundary =  v.split("=")[1]
		data = r.content.split(boundary)
		for d in data:
			if (len(d) >= 1024):
				audio = d.split('\r\n\r\n')[1].rstrip('--')
		with open(path+"response.mp3", 'wb') as f:
			f.write(audio)
                sense.show_letter("!")
		os.system('mpg123 -q {}response.mp3'.format(path, path)) # Writing response and playing response back to user
