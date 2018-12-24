#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime

SDI   = 11
RCLK  = 12
SRCLK = 13

# If you get garbled characters when running this script, you may have wired
# your pins in a non-standard order. You will need to re-map the array below
# to match your pins. See this URL to help get started using the reference. 
# You can also use this to add or modify more characters like I did for the 
# degree symbol for temperature display.
# https://en.wikichip.org/wiki/seven-segment_display/representing_letters

segCode = [
	0x3f, #0
	0x06, #1
	0x5b, #2
	0x4f, #3
	0x66, #4
	0x6d, #5
	0x7d, #6
	0x07, #7
	0x7f, #8
	0x6f, #9
	0x77, #A
	0x7c, #b
	0x39, #C
	0x5e, #d
	0x79, #E
	0x71, #F
	0x3D, #G
	0x76, #H
	0x74, #h
	0x30, #I
	0x1E, #J
	0x38, #L
	0x54, #n
	0x3F, #O
	0x5C, #o
	0x73, #P
	0x67, #q
	0x50, #r
	0x6D, #S
	0x78, #t
	0x3E, #U
	0x1C, #u
	0x6E, #y
	0x00, # off / blank
	0x80, # decimal
	0x63, # degree symbol for temperature
	]

hello_array = [
	0x74, #h
	0x79, #E
	0x38, #L
	0x38, #L
	0x5C, #o
	0x00, # off / blank
	]

def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'

def setup():
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def hc595_shift(dat):
	for bit in range(0, 8):	
		GPIO.output(SDI, 0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		#time.sleep(0.001)  # comment out to remove flicker when seconds advance
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(RCLK, GPIO.LOW)

def countdown():
	diff = datetime.datetime(2018, 12, 25) - datetime.datetime.today()
	days =  "{0:0>2}".format(diff.days)
	hours =  "{0:0>2}".format(diff.seconds/60/60)
	minutes =  "{0:0>2}".format(diff.seconds/60 - (diff.seconds/60/60 * 60))
	now = '{0}{1}{2}'.format(days,hours,minutes)
	for foo in range(0,6):
		hc595_shift(segCode[int(now[foo])])
	time.sleep(6)

def temperature():
        while True:
                for i in range(0, 19):
			hc595_shift(0x00)
			hc595_shift(0x00)
			hc595_shift(segCode[6])
			hc595_shift(segCode[4])
			hc595_shift(segCode[35])
			hc595_shift(segCode[15])
		time.sleep(6)

def scroll_all():
        while True:
                for i in range(0, len(segCode)):
                        hc595_shift(segCode[i])
                        time.sleep(0.8)

def now():
		for bit in range(0,6):
	                countdown=time.strftime( '%H%M%S')
			for foo in range(0,6):
                        	hc595_shift(segCode[int(countdown[foo])])
                	time.sleep(1)

def hello():
        while True:
                for i in range(0, len(hello_array)):
                        hc595_shift(hello_array[i])
                        time.sleep(0.3)

def blank():
		for bit in range(0,1):
			for foo in range(0,6):
                        	hc595_shift(0x00)
                	time.sleep(0.6)


def loop(): # Main loop that calls the various functions
	while True:
		blank()
		now()
		blank()
		countdown()	
#		blank()
#		scroll_all()
#		blank()
#		temperature()
#		hello()


def destroy():   #When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__': #Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
