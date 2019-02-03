import re
import feedparser
import threading
 
temp_scale = '0' # 0 for Farenheit and 1 for Celcius

# Get temperature from AccuWeather
# Example: http://rss.accuweather.com/rss/liveweather_rss.asp?metric=0&locCode=93117
rssfeed = 'http://rss.accuweather.com/rss/liveweather_rss.asp?metric=' + str(temp_scale) + '&locCode=93117'

regex = re.compile('(Currently:.*?)\:*: (\w+)')

def output_temp_numbers(entry):
    #print entry
    f = open("/home/pi/numitron_clock/temperature.txt", "w")
    f.write(entry)

foo = feedparser.parse(rssfeed) # Read page 
for post in foo.entries:  # Read one RSS entry at a time
        try: 
            regex_match = re.search(regex, post.title)
        except:
            print 'URL Error'
        if (regex_match != None):
	    temperature_scale = regex_match.group(2)
	    temperature = temperature_scale.rstrip('F|C')
            output_temp_numbers(temperature)

