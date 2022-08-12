try:
    import RPi.GPIO as GPIO
    from StopLight import RPiStoplight as Stoplight
    #from StopLight import UiStopLightApp as Stoplight
except:
    from StopLight import UiStopLightApp as Stoplight
from WeatherMonitor import BackgroundWeatherMonitor
import threading
import WeatherReporter as weather

windReporter = weather.NoaaWindReporter()
surfReporter = weather.StormGlassSurfReporter()

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