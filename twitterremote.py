#!/usr/bin/python3
from twython import TwythonStreamer,Twython
import time
from datetime import datetime
import pytz
import picamera
import RPi.GPIO as GPIO

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False




class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			determinecommand(data)
			callsremaining	= twitter.get_lastfunction_header('x-rate-limit-remaining')
			print(callsremaining)


	def on_error(self, status_code, data):
		print(status_code)

def determinecommand(data):
	command = 0
	length = 0
	commands = data['text'].split(' ')
	for commander in commands:
		if commander == 'forward':
			command = 1
		elif commander == 'backward':
			command = 2
		elif commander == 'right':
			command = 3
		elif commander == 'left':
			command = 4
		elif commander == 'snapshot':
			command = 5
			docommand(data,command,length)
		elif commander == 'ping':
			command =  6
			docommand(data,command,length)
		elif command > 0 and command < 5 and is_number(commander):
			length = float(commander)
			if length > 60:
				length = 60
			docommand(data,command,length)
			command = 0
			length = 0

def docommand(data,command, length):
	if command == 0:
		time.sleep(0)
	elif command == 1:
		GPIO.output(22, True)
		GPIO.output(24, False)
		GPIO.output(26, False)
		print('going forward for {0:.1f}.'.format(length))
		time.sleep(length)
	elif command == 2:
		GPIO.output(22, False)
		GPIO.output(24, True)
		GPIO.output(26, False)
		print('going backward for {0:.1f}.'.format(length))
		time.sleep(length)
	elif command == 3:
		GPIO.output(22, True)
		GPIO.output(24, True)
		GPIO.output(26, False)
		print('going right for {0:.1f}.'.format(length))
		time.sleep(length)
	elif command == 4:
		GPIO.output(22, False)
		GPIO.output(24, False)
		GPIO.output(26, True)
		print('going left for {0:.1f}.'.format(length))
		time.sleep(length)
	elif command == 5:
		print('for log: trying to display image')

		camera.capture('/balancebot/image.jpg')
		photo = open('/balancebot/image.jpg','rb')

		twitter.update_status_with_media(status='Updated image!' + datetime.now().strftime('%X') + ' #sr04balancebot',media=photo)
		photo.close()

	elif command ==6:
		print('for log: going to retweet')
		twitter.update_status(status=('Hey! @' + data['user']['screen_name'] + ' ' +  datetime.now().strftime('%X')) )


	GPIO.output(22, False)
	GPIO.output(24, False)
	GPIO.output(26, False)



APP_KEY = ''
APP_SECRET = ''
oath_token = ''
oath_token_secret = ''


stream  =  MyStreamer(APP_KEY, APP_SECRET, oath_token, oath_token_secret,300,2,10)
twitter =  twitter = Twython(APP_KEY,APP_SECRET,oath_token,oath_token_secret)

stream.statuses.filter(track='#sr04balancebot')
