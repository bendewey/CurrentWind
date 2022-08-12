import time
from StopLightColors import StopLightColor
from StopLightModes import StopLightMode

class BackgroundWeatherMonitor():
    def __init__(self, stoplight, windReporter, surfReporter):
        self.stoplight = stoplight
        self.isRunning = False
        self.windReporter = windReporter
        self.surfReporter = surfReporter
        self.currentReporter = self.windReporter

    def run(self):
        try:
            # Pause for 1 minute
            #time.sleep(60)
            self.isRunning = True

            while self.isRunning:
                if self.currentReporter.loadRequired():
                    
                    self.stoplight.all_off()
                    if self.stoplight.getMode() == StopLightMode.WIND:
                        self.stoplight.setStatus('Loading Wind')
                        self.currentReporter = self.windReporter
                    else:
                        self.stoplight.setStatus('Loading Surf')
                        self.currentReporter = self.surfReporter

                    self.currentReporter.loadLatest()
                    color = self.currentReporter.calculateRange()
                    self.stoplight.setStatus(self.currentReporter.name + ' is ' + str(self.currentReporter.latest))
                    
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