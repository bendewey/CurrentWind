try:
    import RPi.GPIO as GPIO
    from Interface.RPiStopLight import RPiStoplight as Stoplight
    #from Interface.UiStopLight import UiStopLightApp as Stoplight
except:
    from Interface.UiStopLight import UiStopLightApp as Stoplight
from BackgroundWeatherMonitor import BackgroundWeatherMonitor
from dotenv import load_dotenv
import os
from Reporters import *
import threading

load_dotenv()  # take environment variables from .env.

STATION = os.getenv('STATION', 'fbis1')
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
USE_SAMPLEDATA_FOR_STORMGLASS_API = os.getenv('USE_SAMPLEDATA_FOR_STORMGLASS_API', 'False').lower() in ('true', '1', 't')
LOCATION = os.getenv('LOCATION', '0,0').split(',')

windReporter = NoaaWindReporter(STATION)
surfReporter = StormGlassSurfReporter({'apiKey': STORMGLASS_API_KEY, 'useSampleData': USE_SAMPLEDATA_FOR_STORMGLASS_API, 'lat': LOCATION[0], 'long': LOCATION[1]})

stoplight = Stoplight([windReporter, surfReporter])

monitor = BackgroundWeatherMonitor(stoplight, windReporter, surfReporter)
monitorThread = threading.Thread(target=monitor.run, args=())
monitorThread.start()

def on_closing():
   monitor.kill()
   stoplight.cleanup()

if __name__ == "__main__":
    try:
        stoplight.protocol("WM_DELETE_WINDOW", on_closing)
        stoplight.mainloop()
    except KeyboardInterrupt:
        monitor.kill()
        stoplight.cleanup()

print('Program ended')