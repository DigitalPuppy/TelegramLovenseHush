# Lovense Hush butt plug control through telegram

This simple script allows you to control a Lovense Hush butt plug by sending
commands to a telegram bot.

## Requirements

- A Lovense Hush obviously
- A way to connect the Hush: either a phone (untested) or a Windows PC with the
Lovense bluetooth USB key.
- A computer to run the python script.

## Setup

### Create a telegram bot

Fire up telegram and go talk to @BotFather: type /newbot and follow the
instructions to setup it's name.
BotFather will give you a bot key. Store it in a file named '.botkey' in the
same directory as where you downloaded the hlt.py script.
Then invite your newly created bot to a group, and make it admin (it will only
work if the bot is a group admin, this is a telegram restriction).


### Install Lovense connect and add your Hush toy.

### Locate Lovense connect address and port.

You need to figure out the IP address and port of the lovense app so that the
script can connect to it. There are multiple ways to do that:

Simplest is to run `hlt.py locate` which uses the lovense cloud service to locate it.

If it fails, you will have to figure it out manually:

The IP address is the local address of the device hosting the lovense app. If same
computer as the one running hlt.py, use '127.0.0.1'.

The port is the TCP port on which the lovense app listens. You can run the command
`netstat -ab` as administrator. Look for ports open by the app named 'connect'.
There are multiple ones so you must find the right one by using the command
`hlt.py lovense HOST:PORT`. It will output 'lovense connected' if it works.
For me port was 20010 but I don't know if it's fixed or not.

## Run it!

Simply run `hlt.py run HOST:PORT`, the program will connect your bot and start
listening for commands.

## Commands

   !help
   !ping
   !vibrate intensity duration
   !pattern patternNubmer duration
   !random
   !stop
   
duration is in seconds and capped to 10 (or use '-' to leave on)

intensity is between 1 and 20

patternNumber is between 1 and 4
