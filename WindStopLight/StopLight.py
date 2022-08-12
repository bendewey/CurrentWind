try:
    import RPi.GPIO as GPIO
except:
    print('no RPi')
import time
from tkinter import *
from StopLightModes import StopLightMode

class UiStopLightApp(Tk):
    def __init__(self, reporters):
        super().__init__()
        self.reporters = reporters

        self.geometry("400x420")
        self.configure(background = "grey")
        self.title("UI Stoplight")
        self.resizable(True, True)

        self.create_canvas()
 
    def create_canvas(self):
        # setting up the canvas
        self.title = Label(self, text = "UI Stoplight")
        self.title.config(font = ("Helvetica", 24), background = "grey")
        self.title.pack()


        self.checkVar = IntVar()
        self.switch = Checkbutton(self, text = "Check Surf", variable=self.checkVar, command=self.checkChanged, onvalue=1, offvalue=0, background = "grey")
        self.switch.pack()

        self.canvas = Canvas(width = 300, height = 300, bg = "White")
        self.canvas.pack(pady = 20)
        self.oval = self.canvas.create_oval(200, 100, 100, 200, width = 3, outline ="grey", fill="white")
        
        self.statusText = StringVar()
        self.status = Label(self, textvariable = self.statusText)
        self.status.config(font = ("Helvetica", 14), background = "grey")
        self.status.pack()
    
    def checkChanged(self):
        print('checkChanged')
        self.setStatus('checked' if self.checkVar.get() == 1 else 'unchecked')
        for r in self.reporters:
            r.invalidate()

    def setStatus(self, text):
        self.statusText.set("Status: " + text)

    def getMode(self) -> StopLightMode:
        return StopLightMode.SURF if self.checkVar.get() == 1 else StopLightMode.WIND

    def all_off(self):
        self.canvas.itemconfigure(self.oval, fill = "white")
        
    def red_on(self):
        self.canvas.itemconfigure(self.oval, fill = "red")
        
    def yellow_on(self):
        self.canvas.itemconfigure(self.oval, fill = "yellow")
        
    def green_on(self):
        self.canvas.itemconfigure(self.oval, fill = "green")
        
    def flash(self):
        for _ in range(5):
            self.canvas.itemconfigure(self.oval, fill = "orange")
            time.sleep(0.5)
            self.canvas.itemconfigure(self.oval, fill = "white")
            time.sleep(0.5)
        
    def cleanup(self):
        self.destroy()
        
class RPiStoplight:
    def __init__(self, reporters):
        self.RED_LED_PIN = 22
        self.YELLOW_LED_PIN = 27
        self.GREEN_LED_PIN = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_LED_PIN, GPIO.OUT)
        GPIO.setup(self.YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_LED_PIN, GPIO.OUT)
    
    def mainloop(self):
        while True:
            time.sleep(1)
    
    def getMode(self) -> StopLightMode:
        return StopLightMode.WIND

    def double_flash_leds(self, pin1, pin2, times):
        for _ in range(times):
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
            time.sleep(0.5)

    def protocol(self, msg, error):
        print('noop')

    def setStatus(self, text):
        print('status : ' + text)

    def all_off(self):
        GPIO.output(self.RED_LED_PIN, GPIO.LOW)
        GPIO.output(self.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_LED_PIN, GPIO.LOW)
        
    def red_on(self):
        GPIO.output(self.RED_LED_PIN, GPIO.HIGH)
        GPIO.output(self.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_LED_PIN, GPIO.LOW)
        
    def yellow_on(self):
        GPIO.output(self.RED_LED_PIN, GPIO.LOW)
        GPIO.output(self.YELLOW_LED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_LED_PIN, GPIO.LOW)
        
    def green_on(self):
        GPIO.output(self.RED_LED_PIN, GPIO.LOW)
        GPIO.output(self.YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_LED_PIN, GPIO.HIGH)
        
    def flash(self):
        self.double_flash_leds(self.RED_LED_PIN, self.YELLOW_LED_PIN, 5)
        
    def cleanup(self):
        GPIO.cleanup()