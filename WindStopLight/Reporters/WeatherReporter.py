import datetime
import os
from StopLightColors import StopLightColor

class WeatherReporter:
    def __init__(self):
        self.name = "Weather"
        self.latest = -1
        self.lastChecked = datetime.datetime(2000,1,1)

    def loadRequired(self):
        delta = datetime.datetime.now() - self.lastChecked
        print('checking delta ' + str(delta))
        refreshInMinutes = int(os.getenv('REFRESH_MINUTES', '5'))
        return delta.total_seconds() > refreshInMinutes * 60

    def invalidate(self):
        print(self.name + ' invalidated')
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