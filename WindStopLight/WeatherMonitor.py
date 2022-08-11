import time
from StopLightColors import StopLightColor
import WeatherReporter as weather

windReporter = weather.NoaaWindReporter()
currentReporter = windReporter

def BackgroundWeatherMonitor(stoplight):
    try:
        # Pause for 1 minute
        #time.sleep(60)

        while True:
            if currentReporter.loadRequired():
                stoplight.all_off()
                
                currentReporter.loadLatest()
                color = currentReporter.calculateRange()
                
                if color == StopLightColor.RED:
                    # it's not windy
                    print('Red light')
                    stoplight.red_on()
                elif color == StopLightColor.YELLOW:
                    # it's heating up
                    print('Yellow light')
                    stoplight.yellow_on()
                elif color == StopLightColor.GREEN:
                    # Go kiting!
                    print('Green light')
                    stoplight.green_on()
                else:
                    print('Blink Red/yellow light')
                    stoplight.flash() 
            time.sleep(1)
            
    except KeyboardInterrupt:
        stoplight.cleanup()
    except Exception as e:
        print('App error occurred')
        print(e)