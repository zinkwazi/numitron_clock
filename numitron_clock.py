#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime
from random import randint


# Define the pins on your Raspberry Pi
SER   = 11 # Serial Data input. Pin 11 on the Pi to pin 14 on 74HC595 (DS)
RCLK  = 12 # Storage register clock pin. Pin 12 on the Pi to pin 12 on 74HC595 (STCP / LATCH)
SRCLK = 13 # Shift register clock pin. Pin 13 on the Pi to pin 11 on 74HC595 (SHCP)

TUBES = 6 # Either 4 or 6 depending on the number of display tubes
BLANK = 2 # Nu,ber of .5 second increments to turn the tubes off for betwen functions.
TEMPERATURE_DATA = "/home/pi/numitron_clock/temperature.txt" # Temp file location (you need write permissions for this)

# Countdown target - will display all zeros when done or if in the past.
# NOTE: Target must be less than 99 days away :)
COUNTDOWN_YEAR = 2019
COUNTDOWN_MONTH = 2 
COUNTDOWN_DAY = 4

# If you get garbled characters when running this script, you may have wired
# your pins in a non-standard order. You will need to re-map the array below
# to match your pins. See this URL to help get started using the reference. 
# You can also use this to add or modify more characters like I did for the 
# degree symbol for temperature display.
# https://en.wikichip.org/wiki/seven-segment_display/representing_letters

segments = [
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
	print 'Press Ctrl+C to exit...'

def setup():
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by physical location
	GPIO.setup(SER, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SER, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def hc595_shift(dat): # Shift register function - push the data to the tubes
	for bit in range(0, 8):	
		GPIO.output(SER, 0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(RCLK, GPIO.LOW)

def countdown(): # Count down the days, hours and minutes until target date
	if (datetime.datetime(COUNTDOWN_YEAR, COUNTDOWN_MONTH, COUNTDOWN_DAY)) < (datetime.datetime.today()):
		for foo in range(0,6):
			hc595_shift(segments[0]) # Time is in the past - set tubes to display 0
		time.sleep(6)
	else:
		diff = datetime.datetime(COUNTDOWN_YEAR, COUNTDOWN_MONTH, COUNTDOWN_DAY) - datetime.datetime.today() 
		days =  "{0:0>2}".format(diff.days)
		hours =  "{0:0>2}".format(diff.seconds/60/60)
		minutes =  "{0:0>2}".format(diff.seconds/60 - (diff.seconds/60/60 * 60))
		now = '{0}{1}{2}'.format(days,hours,minutes)
		for foo in range(0,6):
			hc595_shift(segments[int(now[foo])])
		time.sleep(6)

def temperature(): # Display the temperature collected by get_temperature.py
	f = open(TEMPERATURE_DATA, "r") # Read the temperature file
	the_temp=f.read()
	if ("x" in the_temp):
		return None
	else:
		for x in range(0,4):
			for i in range(0, 1): # Still need to account for negative and triple digit temps
				hc595_shift(0x00)
				hc595_shift(0x00)
				hc595_shift(segments[int(the_temp[0])])
				hc595_shift(segments[int(the_temp[1])])
				hc595_shift(segments[35])
				hc595_shift(segments[15])
			time.sleep(1)

def scroll_all(): # Displays all characters in the array
        for x in range(0,1):
                for i in range(0, len(segments)):
                        hc595_shift(segments[i])
                        time.sleep(1)

def scroll_random(): # Quickly flash characters as a divider between other functions
        for x in range(0,1):
                for i in range(0, 9): # How many digits to flash
			bar = randint(1, (len(segments) - 1)) # Pick a random character from the array
                        hc595_shift(segments[(randint(0, bar))])
                        #hc595_shift(segments[i])
			time.sleep(0.07)

def now(): # Display the current time
	for bit in range(0,8):
		current_time=time.strftime('%H%M%S')
		for bar in range(0,6):
			hc595_shift(segments[int(current_time[bar])])
		time.sleep(1)

def flash_chars(): # Flash each character on all tubes
	for bit in range(0,19):
		for bar in range(0,6):
			hc595_shift(segments[bit])
		time.sleep(0.2)

def hello(): # Scroll hello across the displays
        for x in range(0,5):
                for i in range(0, len(hello_array)):
                        hc595_shift(hello_array[i])
                        time.sleep(0.3)

def blank(delay): # Turn off all tubes
	for bit in range(0,BLANK):
		for i in range(0,6):
			hc595_shift(0x00)
		time.sleep(delay)
		#time.sleep(0.33)

def loop(): # Main loop that calls the various functions
	blank(0.33) # Clear the tubes to start
	while True: # Uncomment lines below to run the various functions
		now()
		scroll_random()
		temperature()
		#scroll_random()
		#blank(0.8)
		flash_chars()


def destroy():   # Clean up the GPIO pins gracefully
	GPIO.cleanup()

if __name__ == '__main__': 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
