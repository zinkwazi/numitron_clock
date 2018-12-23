#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime

SDI   = 11
RCLK  = 12
SRCLK = 13

segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71,0x80,0x63,0x00]
#0,1,2,3,4,5,6,7,8,9,A,b,C,d,E,F,degree symbol
#segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]

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
		time.sleep(0.001)
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)

def countdown():
	diff = datetime.datetime(2018, 12, 25) - datetime.datetime.today()
	days =  "{0:0>2}".format(diff.days)
	hours =  "{0:0>2}".format(diff.seconds/60/60)
	minutes =  "{0:0>2}".format(diff.seconds/60 - (diff.seconds/60/60 * 60))
	then = '{0}{1}{2}'.format(days,hours,minutes)
	for foo in range(0,6):
		hc595_shift(segCode[int(then[foo])])
	time.sleep(9)

def then():
		for bit in range(0, 10):
	                countdown=time.strftime( '%H%M%S')
			for foo in range(0,6):
                        	hc595_shift(segCode[int(countdown[foo])])
                	time.sleep(0.9)

def blank():
		for bit in range(0, 1):
			for foo in range(0,6):
                        	hc595_shift(segCode[18])
                	time.sleep(0.6)

def phoebe():
		for foo in range(0,6):
			hc595_shift(segCode[18])
		time.sleep(0.6)
	
def loop():
	while True:
		countdown()	
		blank()
		then()
		blank()


def destroy():   #When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__': #Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
