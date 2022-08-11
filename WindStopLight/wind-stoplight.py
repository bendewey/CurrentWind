import RPi. GPIO as GPIO
import time
import requests
import json
import re

def double_flash_leds(pin1, pin2, times):
    for _ in range(times):
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        time.sleep(0.5)

  
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


def getwind_noaa():
    try:
        print('retrieving wind from noaa')
        station = 'fbis1'
        r = requests.get("http://www.ndbc.noaa.gov/station_page.php?station=" + station)
        pageContent = r.text
        x = re.search("Continuous Winds((.|\\r|\\n)(?!\\d+\\skts))*\\s*((\\d+)\\s+kts)", pageContent)
        wind = int(x.groups()[3])
        print('wind is ' + str(wind))
        return wind;
    except:
        return -1

def getwind_api():
    print('retrieving wind')
    r = requests.get('https://currentwind.azurewebsites.net/WeatherForecast?station=fbis1')
    forecast = json.loads(r.text)
    wind = int(forecast["windSpeed"])
    print('wind is ' + str(wind))
    return wind;

RED_LED_PIN = 22
YELLOW_LED_PIN = 27
GREEN_LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# Pause for 1 minute
time.sleep(60)

try:
    while True:
        wind = getwind_noaa()
        if wind == -1:
            print('Blink Red/yellow light')
            double_flash_leds(RED_LED_PIN, YELLOW_LED_PIN, 5)  
        elif wind < 10:
            # it's not windy
            print('Red light')
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)
        elif wind < 15:
            # it's heating up
            print('Yellow light')
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)
        else:
            # Go kiting!
            print('Green light')
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
        # Pause for 5 minutes
        time.sleep(60*5)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(GREEN_LED_PIN, GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as e:
    print('Error occurred')
    print(e)
print('Program ended')