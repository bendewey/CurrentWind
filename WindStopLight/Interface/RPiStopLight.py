try:
    import RPi.GPIO as GPIO
except:
    print('no RPi')
import time
from StopLightModes import StopLightMode

class RPiStoplight:
    RED_LED_PIN = 22
    YELLOW_LED_PIN = 27
    GREEN_LED_PIN = 17
    SWITCH_PIN = 23

    def __init__(self, reporters):
        self.switchStatus = False
        self.reporters = reporters
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RPiStoplight.RED_LED_PIN, GPIO.OUT)
        GPIO.setup(RPiStoplight.YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(RPiStoplight.GREEN_LED_PIN, GPIO.OUT)
        GPIO.setup(RPiStoplight.SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(RPiStoplight.SWITCH_PIN, GPIO.BOTH, callback=self.switch_callback)
    
    def switch_callback(self):
        for r in self.reporters:
            r.invalidate()

    def mainloop(self):
        while True:
            time.sleep(1)
    
    def getMode(self) -> StopLightMode:
        return StopLightMode.WIND if GPIO.input(RPiStoplight.SWITCH_PIN) else StopLightMode.SURF

    def double_flash_leds(self, pin1, pin2, times):
        for _ in range(times):
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
            time.sleep(0.5)

    def protocol(self, msg, error):
        pass

    def setStatus(self, text):
        pass

    def all_off(self):
        GPIO.output(RPiStoplight.RED_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.GREEN_LED_PIN, GPIO.LOW)
        
    def red_on(self):
        GPIO.output(RPiStoplight.RED_LED_PIN, GPIO.HIGH)
        GPIO.output(RPiStoplight.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.GREEN_LED_PIN, GPIO.LOW)
        
    def yellow_on(self):
        GPIO.output(RPiStoplight.RED_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.YELLOW_LED_PIN, GPIO.HIGH)
        GPIO.output(RPiStoplight.GREEN_LED_PIN, GPIO.LOW)
        
    def green_on(self):
        GPIO.output(RPiStoplight.RED_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(RPiStoplight.GREEN_LED_PIN, GPIO.HIGH)
        
    def flash(self):
        self.double_flash_leds(RPiStoplight.RED_LED_PIN, RPiStoplight.YELLOW_LED_PIN, 5)
        
    def cleanup(self):
        GPIO.cleanup()