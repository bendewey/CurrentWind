try:
    import RPi.GPIO as GPIO
except:
    print('no RPi')
import time
from tkinter import Tk
from tkinter import Label
from tkinter import Canvas

class UiStopLightApp(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.configure(background = "grey")
        self.title("UI Stoplight")
        self.resizable(True, True)

        self.create_canvas()

        
    def create_canvas(self):
        # setting up the canvas
        self.title = Label(self, text = "UI Stoplight")
        self.title.config(font = ("Helvetica", 24), background = "grey")
        self.title.pack()

        self.canvas = Canvas(width = 300, height = 300, bg = "White")
        self.canvas.pack(pady = 20)
        self.oval = self.canvas.create_oval(200, 100, 100, 200, width = 3, outline ="grey", fill="red")
    
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
    def __init__(self):
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
    
    def double_flash_leds(self, pin1, pin2, times):
        for _ in range(times):
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
            time.sleep(0.5)

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