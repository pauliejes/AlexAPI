# Alexa Personal Assitant for Raspberry Pi
# Coded by Simon Beal and Matthew Timmons-Brown for "The Raspberry Pi Guy" YouTube channel
# Built upon the work of Sam Machin, (c)2016
# Feel free to look through the code, try to understand it & modify as you wish!
# The installer MUST be run before this code.

#!/usr/bin/python
import sys
import time
from sense_hat import SenseHat
import os
import alsaaudio
import wave
import numpy
import copy
import requests
import json
import base64
import urllib
from evdev import InputDevice, list_devices, ecodes

import alexa_helper # Import the web functions of Alexa, held in a separate program in this directory

print "Welcome to Alexa. I will help you in anyway I can.\n  Press Ctrl-C to quit"

sense = SenseHat() # Initialise the SenseHAT
sense.clear()  # Blank the LED matrix

auth = "Basic %s" % base64.b64encode("%s:%s" % ("AlexAPI", "hello123"))
headers = { 'Authorization': auth,
        'content-type': 'application/json',
        'X-Experience-API-Version': '1.0.2'
}
stmt_endpoint = "https://lrs.adlnet.gov/xapi/statements"

# POST EXAMPLE
post_payload = {
        "actor": {
            "mbox": "mailto:alexAPI@amazon.com"
        },
        "verb": {
            "id": "http://adlnet.gov/expapi/verbs/passed",
            "display": {
                "en": "verbed"
            }
        },
        "object": {
            "id": "http://activity.com/id"
        },

        "result": {
            "success": True
        }
    }


# Search for the SenseHAT joystick
found = False
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True 
        break

# Exit if SenseHAT not found
if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()

# Initialise audio buffer
audio = ""
inp = None

# We're British and we spell "colour" correctly :) Colour code for RAINBOWZ!!
colours = [[255, 0, 0], [255, 0, 0], [255, 105, 0], [255, 223, 0], [170, 255, 0], [52, 255, 0], [0, 255, 66], [0, 255, 183]]

# Loudness for highest bar of RGB display
max_loud = 1024

# Given a "loudness" of speech, convert into RGB LED bars and display - equaliser style
def set_display(loudness):
    mini = [[0,0,0]]*8
    brightness = max(1, min(loudness, max_loud) / (max_loud/8))
    mini[8-brightness:] = colours[8-brightness:]
    display = sum([[col]*8 for col in mini], [])
    sense.set_pixels(display)

# When button is released, audio recording finishes and sent to Amazon's Alexa service
def release_button():
    global audio, inp
    sense.set_pixels([[0,0,0]]*64)
    w = wave.open(path+'recording.wav', 'w') # This and following lines saves voice to .wav file
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    sense.show_letter("?") # Convert to question mark on display
    alexa_helper.alexa(sense) # Call upon alexa_helper program (in this directory)
    sense.clear() # Clear display
    inp = None
    audio = ""

# When button is pressed, start recording
def press_button():
    global audio, inp
    try:
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, alexa_helper.device)
    except alsaaudio.ALSAAudioError:
        print('Audio device not found - is your microphone connected? Please rerun program')
        sys.exit()
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    audio = ""
    l, data = inp.read()
    if l:
        audio += data
        post_resp = requests.post(stmt_endpoint, data=json.dumps(post_payload), headers=headers, verify=False)
        print post_resp.content
        print post_resp.status_code


# Whilst button is being pressed, continue recording and set "loudness"
def continue_pressed():
    global audio, inp
    l, data = inp.read()
    if l:
        audio += data
        a = numpy.fromstring(data, dtype='int16') # Converts audio data to a list of integers
        loudness = int(numpy.abs(a).mean()) # Loudness is mean of amplitude of sound wave - average "loudness"
        set_display(loudness) # Set the display to show this "loudness"

# Event handler for button
def handle_enter(pressed):
    handlers = [release_button, press_button, continue_pressed] # 0=released, 1=pressed, 2=held
    handlers[pressed]()

# Continually loops for events, if event detected and is the middle joystick button, call upon event handler above
def event_loop():
    try:
        for event in dev.read_loop(): # for each event
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_ENTER: # if event is a key and is the enter key (middle joystick)
                handle_enter(event.value) # handle event
    except KeyboardInterrupt: # If Ctrl+C pressed, pass back to main body - which then finishes and alerts the user the program has ended
        pass

if __name__ == "__main__": # Run when program is called (won't run if you decide to import this program)
    while alexa_helper.internet_on() == False:
        print "."
    token = alexa_helper.gettoken()
    path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
    os.system('mpg123 -q {}hello.mp3'.format(path, path)) # Say hello!
    event_loop()
    print "\nYou have exited Alexa. I hope that I was useful. To talk to me again just type: python main.py"
