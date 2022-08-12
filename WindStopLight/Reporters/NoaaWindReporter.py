import datetime
import re
import requests
import Reporters.WeatherReporter as WeatherReporter

class NoaaWindReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "NOAA Wind"

    def loadLatest(self):
        try:
            print('retrieving wind from noaa')
            station = 'fbis1'
            r = requests.get("http://www.ndbc.noaa.gov/station_page.php?station=" + station)
            pageContent = r.text
            x = re.search("Continuous Winds((.|\\r|\\n)(?!\\d+\\skts))*\\s*((\\d+)\\s+kts)", pageContent)
            wind = int(x.groups()[3])
            print('wind is ' + str(wind))
            self.latest = wind
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest -1
            self.lastChecked = datetime.datetime.now()
