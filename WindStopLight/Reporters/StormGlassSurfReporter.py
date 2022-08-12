import datetime
from logging import raiseExceptions
import requests
import json
from StopLightColors import StopLightColor
import Reporters.WeatherReporter as WeatherReporter
from dotenv import load_dotenv

class StormGlassSurfReporter(WeatherReporter):
    def __init__(self, config):
        super().__init__()
        self.name = "StormGlass Surf"
        if type(config) is dict:
            print('converting to anon')
            self.config = type('',(object,),config)
        else:
            self.config = config

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
        json_data = json.loads(json_text)
        return json_data

    def callApi(self):
        beginHr, endHr = self.getDateRangeForApi()
        print('retrieving surf from stormglass')
        response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': self.config.lat,
            'lng': self.config.long,
            'params': 'waveHeight,wavePeriod',
            'start': beginHr.isoformat() + "+00:00",
            'end': endHr.isoformat() + "+00:00",
            'source': 'sg',
        },
        headers={
            'Authorization': self.config.apiKey
        }
        )

        # Do something with response data.
        return response.json()

    def loadLatest(self):
        try:
            if self.config.useSampleData:
                json_data = self.sampleApi()
            else:
                json_data = self.callApi()
                        
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


