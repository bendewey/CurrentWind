import datetime
from logging import raiseExceptions
import requests
import json
from StopLightColors import StopLightColor
import Reporters.WeatherReporter as WeatherReporter

class StormGlassSurfReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "StormGlass Surf"

    def getDateRangeForApi(self):
        now = datetime.datetime.now()
        beginHr = datetime.datetime(now.year, now.month, now.day, now.hour)
        if (now.hour > 20):
            endHr = datetime.datetime(now.year, now.month, now.day+1, now.hour + 3 - 24, 59)
        else:
            endHr = datetime.datetime(now.year, now.month, now.day, now.hour + 3, 59)
        return beginHr, endHr

    def sampleApi(self):
        json_text = """{
  "hours": [
    {
      "time": "2018-01-19T17:00:00+00:00",
      "waveHeight": {
        "noaa": 2.1,
        "sg": 2.3
      },
      "wavePeriod": {
        "noaa": 9,
        "sg": 9
      }
    }
  ],
  "meta": {
    "dailyQuota": 50,
    "lat": 58.7984,
    "lng": 17.8081,
    "requestCount": 1
  }
}"""    
        print(json_text)
        json_data = json.loads(json_text)
        return json_data

    def callApi(self):
        apikey = '14691b2a-18c2-11ed-a3aa-0242ac130002-14691ba2-18c2-11ed-a3aa-0242ac130002'
        lat = 32.78498
        long = -79.78441
        beginHr, endHr = self.getDateRangeForApi()
        print('retrieving surf from stormglass')
        response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': lat,
            'lng': long,
            'params': 'waveHeight,wavePeriod',
            #'start': beginHr.isoformat() + "+00:00",
            #'end': endHr.isoformat() + "+00:00",
            #'start': "2022-08-12T14:00:00+00:00",
            #'end': "2022-08-12T17:59:00+00:00",
            'start': '2022-08-10T18:00:00+00:00',
            'end': '2022-08-10T18:59:00+00:00',
            'source': 'sg',
        },
        headers={
            'Authorization': apikey
        }
        )

        # Do something with response data.
        return response.json()

    def loadLatest(self):
        try:
            json_data = self.sampleApi()
            print(json_data)
            
            if "errors" in json_data:
                raise Exception(json_data['errors']['key'])
            else:
                waveHeight = json_data['hours'][0]['waveHeight']['sg']
                wavePeriod = json_data['hours'][0]['wavePeriod']['sg']
                print('h=' + str(waveHeight) + ', p=' + str(wavePeriod))
                self.latest = (waveHeight, wavePeriod)
                print(self.latest)
                self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('Surf error occurred')
            print(e)
            self.latest = (-1, -1)
            self.lastChecked = datetime.datetime.now()

    def calculateRange(self) -> StopLightColor:
        waveHeight, wavePeriod = self.latest
        if waveHeight == -1:
            return StopLightColor.ERROR
        elif waveHeight < 1 or wavePeriod < 6:
            return StopLightColor.RED
        elif waveHeight < 3 and wavePeriod < 8:
            return StopLightColor.YELLOW
        else:
            return StopLightColor.GREEN


