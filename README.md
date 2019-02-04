# Raspberry Pi Numitron Clock

6 digit Numitron tube clock
- Six digit clock - hours / minute / seconds
- Time - uses NTP to stay very accurate
- Count down days, hours and minitues to a target date
- Display temperature in farenheit or celcius
- Scroll text across tubes
- Random scramble function to separate time / temp etc 

74HC595 serial to parallel shift register ICs driven by a Raspberry Pi Zero

The Numitron IV-9 (AKA IV-9 / ИВ-9 / Reflector/ Sovtec Glühfaden Röhre) tubes are low voltage
and run easily from the 5V rail on the Raspberry Pi (and Arduino for that matter)

This is a great project for a simple clock - you can adaprt it to use just one tube or add
more than six tubes and make a Divergence Meter :)

Wiring the 74HC595 chips is easy and well documented on line. This is one of the better
examples out there: https://www.arduino.cc/en/Tutorial/ShiftOut showing how to connect the 595s.

-- 

Send fixes, questions or suggestions :)

Greg Lawler 
https://zinkwazi.com
