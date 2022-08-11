import RPi.GPIO as GPIO
import time
from tkinter import Tk
from tkinter import Canvas
import threading
 


class UiStopLight:
    def runwindow(self, window):
        window.mainloop()
        
    def init(self):
        self.window = Tk()
        self.window.geometry("400x400")
        self.window.configure(background = "grey")
        self.window.title("UI Stoplight")
        self.window.resizable(False, False)
         
        # setting up the canvas
        self.canvas = Canvas(width = 350, height = 350, bg = "white")
        self.canvas.pack(pady = 20)
         
        self.canvas.create_text(175, 20, text = "Stoplight", font = ("Arial", 30))
        self.oval = self.canvas.create_oval(175, 100, 100, 175, width = 3, fill="red")
        
        #t = threading.Thread(target=self.runwindow, args=self.window)
        #t.start();
        self.window.mainloop()
    
    def all_off(self):
        self.canvas.itemconfigure(self.oval, fill = "white")
        
    def red_on(self):
        self.canvas.itemconfigure(self.oval, fill = "red")
        
    def yellow_on(self):
        self.canvas.itemconfigure(self.oval, fill = "yellow")
        
    def green_on(self):
        self.canvas.itemconfigure(self.oval, fill = "green")
        
    def flash(self):
        self.canvas.itemconfigure(self.oval, fill = "purple")
        
    def cleanup(self):
        self.window.exit()
        
class RPiStoplight:
    def init(self):
        self.RED_LED_PIN = 22
        self.YELLOW_LED_PIN = 27
        self.GREEN_LED_PIN = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_LED_PIN, GPIO.OUT)
        GPIO.setup(self.YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_LED_PIN, GPIO.OUT)
        
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