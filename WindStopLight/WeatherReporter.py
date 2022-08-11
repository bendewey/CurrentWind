from StopLightColors import StopLightColor
import requests
import re
import datetime

class WeatherReporter:
    def __init__(self):
        self.latest = -1
        self.lastChecked = datetime.datetime(2000,1,1)

    def loadRequired(self):
        delta = datetime.datetime.now() - self.lastChecked
        print('checking delta ' + str(delta))
        return delta.total_seconds() > 5 * 60

    def invalidate(self):
        self.latest = -1
        self.lastChecked = datetime.datetime(2000,1,1)
        
    def loadLatest(self):
        self.latest = -1
        self.lastChecked = datetime.datetime.now()

    def calculateRange(self) -> StopLightColor:
        if self.latest == -1:
            return StopLightColor.ERROR
        elif self.latest < 10:
            return StopLightColor.RED
        elif self.latest < 15:
            return StopLightColor.YELLOW
        else:
            return StopLightColor.GREEN

class NoaaWindReporter(WeatherReporter):
    def loadLatest(self):
        try:
            print('retrieving wind from noaa')
            station = 'fbis1'
            r = requests.get("http://www.ndbc.noaa.gov/station_page.php?station=" + station)
            pageContent = r.text
            x = re.search("Continuous Winds((.|\\r|\\n)(?!\\d+\\skts))*\\s*((\\d+)\\s+kts)", pageContent)
            wind = int(x.groups()[3])
            wind = 16
            print('wind is ' + str(wind))
            self.latest = wind;
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest -1
            self.lastChecked = datetime.datetime.now()
