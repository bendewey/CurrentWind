import StopLight
import time
import requests
import json
from StopLightColors import StopLightColor
import WeatherReporter as weather



def getsurf_stormglass():
    try:
        apikey = '14691b2a-18c2-11ed-a3aa-0242ac130002-14691ba2-18c2-11ed-a3aa-0242ac130002'
        lat = 32.78498
        long = -79.78441
                
        print('retrieving surf from stormglass')
        #r = requests.get("http://www.ndbc.noaa.gov/station_page.php?station=" + station)
        response = requests.get(
          'https://api.stormglass.io/v2/weather/point',
          params={
            'lat': lat,
            'lng': long,
            'params': 'waveHeight,wavePeriod',
            'start': '2022-08-10T18:00:00+00:00',
            'end': '2022-08-10T18:59:00+00:00',
            'source': 'sg',
          },
          headers={
            'Authorization': apikey
          }
        )

        # Do something with response data.
        json_data = response.json()
        waveHeight = json_data['hours'][0]['waveHeight']['sg']
        wavePeriod = json_data['hours'][0]['wavePeriod']['sg']
        print('h=' + str(waveHeight) + ', p=' + str(wavePeriod))
        #forecast = json.loads(r.text)
        #       wind = int(forecast["wind"])
        #      print('wind is ' + str(wind))
        return waveHeight, wavePeriod
    except Exception as e:
        print('Error occurred')
        print(e)
        return -1, -1

def getwind_api():
    print('retrieving wind')
    r = requests.get('https://currentwind.azurewebsites.net/WeatherForecast?station=fbis1')
    forecast = json.loads(r.text)
    wind = int(forecast["windSpeed"])
    print('wind is ' + str(wind))
    return wind;

#stoplight = StopLight.RPiStoplight()
stoplight = StopLight.UiStopLight()
stoplight.init()

# Pause for 1 minute
#time.sleep(60)
windReporter = weather.NoaaWindReporter()
currentReporter = windReporter

try:
    while True:
        if currentReporter.loadRequired():
            stoplight.all_off()
            
            currentReporter.loadLatest()
            color = currentReporter.calculateRange()
            
            if color == StopLightColor.RED:
                # it's not windy
                print('Red light')
                stoplight.red_on()
            elif color == StopLightColor.YELLOW:
                # it's heating up
                print('Yellow light')
                stoplight.yellow_on()
            elif color == StopLightColor.GREEN:
                # Go kiting!
                print('Green light')
                stoplight.green_on()
            else:
                print('Blink Red/yellow light')
                stoplight.flash() 
        time.sleep(1)
        
except KeyboardInterrupt:
    stoplight.cleanup()
except Exception as e:
    print('App error occurred')
    print(e)
print('Program ended')