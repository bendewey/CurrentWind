import time
from StopLightColors import StopLightColor
import WeatherReporter as weather

windReporter = weather.NoaaWindReporter()
currentReporter = windReporter

class BackgroundWeatherMonitor():
    def __init__(self, stoplight):
        self.stoplight = stoplight
        self.isRunning = False

    def run(self):
        try:
            # Pause for 1 minute
            #time.sleep(60)
            self.isRunning = True

            while self.isRunning:
                if currentReporter.loadRequired():
                    self.stoplight.all_off()
                    self.stoplight.setStatus('Loading Weather')

                    currentReporter.loadLatest()
                    color = currentReporter.calculateRange()
                    self.stoplight.setStatus('')
                    
                    if color == StopLightColor.RED:
                        # it's not windy
                        print('Red light')
                        self.stoplight.red_on()
                    elif color == StopLightColor.YELLOW:
                        # it's heating up
                        print('Yellow light')
                        self.stoplight.yellow_on()
                    elif color == StopLightColor.GREEN:
                        # Go kiting!
                        print('Green light')
                        self.stoplight.green_on()
                    else:
                        print('Blink Red/yellow light')
                        self.stoplight.flash() 
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stoplight.cleanup()
        except Exception as e:
            print('App error occurred')
            print(e)

    def kill(self):
        self.isRunning = False