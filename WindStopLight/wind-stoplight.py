try:
    import RPi.GPIO as GPIO
    from StopLight import RPiStoplight as Stoplight
except:
    from StopLight import UiStopLightApp as Stoplight
import time
from WeatherMonitor import BackgroundWeatherMonitor
import requests
import json
import threading




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

stoplight = Stoplight()

monitor = BackgroundWeatherMonitor(stoplight)
monitorThread = threading.Thread(target=monitor.run, args=())
monitorThread.start()

def on_closing():
   monitor.kill()
   stoplight.cleanup()

if __name__ == "__main__":
    stoplight.protocol("WM_DELETE_WINDOW", on_closing)
    stoplight.mainloop()

print('Program ended')