import re
import feedparser
import threading

temperature_file_path = "/home/pi/numitron_clock/temperature.txt"
temp_scale = '0' # 0 for Farenheit and 1 for Celcius
zip_code = "93117" # Zip code or city
#zip_code = "New%20York" # Example - use %20 for spaces in city names

# Get temperature from AccuWeather
# Example URL: http://rss.accuweather.com/rss/liveweather_rss.asp?metric=0&locCode=93117
rssfeed = 'http://rss.accuweather.com/rss/liveweather_rss.asp?metric='+ temp_scale +'&locCode=' + zip_code
#rssfeed = 'http://zinkwazi.com/tools/temperature.xml'
regex = re.compile('(Currently:.*?)\:*: (\w+)') # Find the temperature line
#regex = re.compile('(Currently:.*?)\:*: ((-|)\w+)') # Find the temperature line

def output_temp_numbers(entry): # Write temperature digits to the file
    f = open(temperature_file_path, "w")
    f.write(entry)

foo = feedparser.parse(rssfeed) # Read RSS page 
if foo.bozo: # Put xx in the file in case of error
        output_temp_numbers("xx")
	exit()

for post in foo.entries:  # Read one RSS entry at a time
        try: 
            regex_match = re.search(regex, post.title)
        except:
            print 'URL Error'
        if (regex_match != None):
	    temperature_scale = regex_match.group(2)
	    temperature = temperature_scale.rstrip('F|C')
            output_temp_numbers(temperature)
exit()
