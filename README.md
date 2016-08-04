# AlexAPI
Integrating xAPI with amazon Alexa

## What you'll need

* [Raspberry Pi](https://www.amazon.com/Raspberry-Pi-RASP-PI-3-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_4?s=pc&ie=UTF8&qid=1470328238&sr=1-4&keywords=raspberry+pi+3) (this project uses RPi3 model B+, but will work with RPi2 B+ and up)
* Usb Microphone
* Speakers with 3.5mm audio cable input
* [Raspberry Pi Sense Hat](https://www.amazon.com/Raspberry-Pi-Sense-HAT-AstroPi/dp/B014HDG74S/ref=sr_1_2?ie=UTF8&qid=1470328199&sr=8-2&keywords=raspberry+pi+sense+hat)
* Amazon Developers Account. [(easily created here)](https://developer.amazon.com)

## Install Raspbian Jessie

If you havent installed Raspbian on your Pi, follow install instructions [here](https://github.com/pauliejes/AlexAPI/blob/master/installRaspian.md)

## Setup

1.) Sign into [Amazon developer console](https://developer.amazon.com) and navigate to the Alexa tab.

2.) Once there click 'Get Started' On the Alexa Voice Service option.

3.) Now Register a product type. Register as Device, not application.

* Enter Device Type ID, and Display name. Make note of spelling and capitolization, you'll need these names later. Click next
* Under Security Profile, select 'Create a new profile', give your profile a name (I recommend using the same name as Device ID) and description (Use the same name again). Click next. Keep this page open for later use
* Navigate to the Web Settings tab. Next to 'Allowed Orgins', click 'Add Another' and type http://localhost:5000. Again click add another and enter the ip address of your raspberry pi like so: http://your.rpi.ip.addr:5000
* Now on the page, find 'Allowed Return URLs' and click 'Add Another'. Copy the same two fields from above, but this time add /code after. For example http://localhost:5000 would now be http://localhost:5000/code and http://your.rpi.ip.addr:5000 would be http://your.rpi.ip.addr:5000/code. Click next
* Complete required fields as necessary, nothing really to change here, use Category: Other. Click next.
* Go back to security profile by clicking edit on your newly created product.

4.) SSH into Pi and get ready to run some commands.

## Installing Alexa

1.) Clone this project <code>git clone https://github.com/pauliejes/AlexAPI.git</code>

2.) cd into new directory <code>cd AlexAPI</code>

3.) run <code>sudo ./setup.sh</code>
* From here you will be promped for the ProductID you set up earlier. Enter it exactly as it appears in your developer console.
* Next you will be asked to enter your Security Profile Description. Enter it exactly as it appears in your developer console.
* Next, copy and paste your Security Profile ID, Client ID, and Client Secrete as promped.
* Now open up a web browser and enter your PI's Ip address followed by :5000, you should be greeted by a login from amazon.
* Login and agree to terms and conditions. You should see a long refresh token which is automatically added to the configuration so you do not need it. Exit the browser, then exit the setup script.

4.) Type <code>python main.py</code>

5.) If eveything goes smoothly, you should be greeted by Alexa.

## How to use

To prompt Alexa, hold down the Joystick and ask your question.

##xAPI

Everytime you ask Alexa a question, she will send a statement to the ADL LRS using xAPI.

Currently the statement is generic and more proof of concept, but will be expanded to hold more information in the future.

Check out the python code in main.py
