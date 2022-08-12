import time
import tkinter
import customtkinter
from StopLightModes import StopLightMode

class UiStopLightApp(customtkinter.CTk):
    def __init__(self, reporters):
        super().__init__()
        self.reporters = reporters

        self.geometry("400x420")
        self.configure(background = "grey")
        self.title("UI Stoplight")
        self.resizable(True, True)
        
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.create_canvas()
 
    def create_canvas(self):
        # setting up the canvas
        self.title = customtkinter.CTkLabel(self, text = "Stoplight")
        self.title.configure(font = ("Helvetica", 24), background = "grey")
        self.title.pack()

        self.checkVar = tkinter.IntVar()
        self.switch = customtkinter.CTkCheckBox(self, text = "Check Surf", variable=self.checkVar, command=self.checkChanged, onvalue=1, offvalue=0, background = "grey")
        self.switch.pack()

        self.canvas = customtkinter.CTkCanvas(width = 300, height = 300, bg = "White")
        self.canvas.pack(pady = 20)
        self.oval = self.canvas.create_oval(200, 100, 100, 200, width = 3, outline ="grey", fill="white")
        
        self.statusText = tkinter.StringVar()
        self.status = customtkinter.CTkLabel(self, textvariable = self.statusText)
        self.status.configure(font = ("Helvetica", 14), background = "grey")
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