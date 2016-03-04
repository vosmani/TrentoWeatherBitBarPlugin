#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# TODO: better compatibility with other OS X versions / python frameworks
from lxml import html
import requests

# <bitbar.title>University of Trento Weather Service</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Venet Osmani</bitbar.author>
# <bitbar.author.github>vosmani</bitbar.author.github>
# <bitbar.desc>Displays real-time weather data (updated every 20 mins) in your OS X menu bar. The data is parsed from Molino Vittoria weather station hosted at University of Trento (http://www.ing.unitn.it/~prometeo/Dati.htm)</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/vosmani/TrentoWeatherBitBarPlugin/master/UniTN-dati-tempo.png</bitbar.image>
# <bitbar.dependencies>python3,lxml,requests</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/vosmani/TrentoWeatherBitBarPlugin</bitbar.abouturl>

# script to send a request to UNITN weather station and parse individual weather elements using xpath

WEATHER_SERVICE_URL = 'http://www.ing.unitn.it/~prometeo/Dati.htm'

try: # needed for network connections (e.g. website unavailable or no Internet connection
    page = requests.get(WEATHER_SERVICE_URL)
    tree = html.fromstring(page.text)

    # array of weather data
    resp = tree.xpath('/html/body/p/font/table/tr/td[2]/table[2]/tr/td[2]/font/text()')
    
    # last updated date
    resp2 = tree.xpath('/html/body/p/font/table/tr/td[2]/table[1]/tr/td[1]/font/text()')
    
    # last updated time
    resp3 = tree.xpath('/html/body/p/font/table/tr/td[2]/table[1]/tr/td[2]/font/text()')


    # define limits, above which the values will show in red
    TEMP_LIM_LOWER = '0'
    TEMP_LIM_UPPER = '33'
    HUM_LIM = '80'
    PRECIP_LIM = '0'
    WIND_SPEED_LIM = '5'

    FONT_COLOR = '#000000'	# default font color - black
    FONT_COLOR_TEMP = '#000000'
    FONT_COLOR_HUM = '#000000'
    FONT_COLOR_PRECIP = '#000000'
    FONT_COLOR_WIND_SPEED = '#000000'

    # need to convert to floats as the lxml responses are strings
    if float(resp[0].strip()) < float(TEMP_LIM_LOWER) or float(resp[0].strip()) > float(TEMP_LIM_UPPER):
        FONT_COLOR_TEMP = '#FF0000'  # RED font color

    if float(resp[1].strip()) > float(HUM_LIM):
        FONT_COLOR_HUM = '#FF0000'	# RED font color

    if float(resp[3].strip()) > float(PRECIP_LIM):
        FONT_COLOR_PRECIP = '#FF0000'

    if float(resp[5].strip()) > float(WIND_SPEED_LIM):
        FONT_COLOR_WIND_SPEED = '#FF0000'



    print ("T:", resp[0].strip(), " | font=UbuntuMono-Bold color=",FONT_COLOR_TEMP," size=11")
    print ("H:", resp[1].strip(), " | font=UbuntuMono-Bold color=",FONT_COLOR_HUM," size=11")
    print ("P:", resp[3].strip(), " | font=UbuntuMono-Bold color=",FONT_COLOR_PRECIP," size=11")
    print ("W:", resp[5].strip(), " | font=UbuntuMono-Bold color=",FONT_COLOR_WIND_SPEED," size=11")

    print ("---")
    
    print ("Temperature:\t",resp[0].strip(), " C", " | color=",FONT_COLOR_TEMP)
    print ("Humidity:\t",resp[1].strip(), " %", " | color=",FONT_COLOR_HUM)
    print ("Precipitation:\t",resp[3].strip(), " mm", " | color=",FONT_COLOR_PRECIP)
    print ("Radiation:\t",resp[4].strip(), " W/m2", " | color=",FONT_COLOR)
    print ("Wind Speed:\t",resp[5].strip(), " m/s", " | color=",FONT_COLOR_WIND_SPEED)
    print ("Wind Direction:\t",resp[6].strip(), " N", " | color=",FONT_COLOR)
    print ("Pressure:\t",resp[2].strip(), " hPa", " | color=",FONT_COLOR)
    print ("Last update:\t", resp3[1])

except Exception as ex:
    print ("Error! | font=UbuntuMono-Bold color=#FF0000 size=11")
    print ("---")
    print ("An error occurred: ", type(ex).__name__, "| color=#FF0000")

