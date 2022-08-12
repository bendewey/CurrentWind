try:
    import RPi.GPIO as GPIO
    from Interface.RPiStopLight import RPiStoplight as Stoplight
    #from Interface.UiStopLight import UiStopLightApp as Stoplight
except:
    from Interface.UiStopLight import UiStopLightApp as Stoplight
import BackgroundWeatherMonitor
import threading
from Reporters import *

windReporter = NoaaWindReporter()
surfReporter = StormGlassSurfReporter()

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