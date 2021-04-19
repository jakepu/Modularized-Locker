import tkinter as tk
from keypad import KeyPad as keypad
from locker_communication import open_locker
from mysql_link import assign_locker
from mysql_link import unassign_locker
import RPi.GPIO as GPIO 

#import RPi.GPIO as GPIO

LARGE_FONT= ("Verdana", 12)
#GPIO.setmode(GPIO.BOARD)
pin0=0
pin1=1
pin2=2
pin3=3

setup_mode=False





pad=keypad()
address=0000


class locker:
    address=1000
    occupied=True
    username=''
    def __init__(self, address, occupied):
        self.addresss=address
        self.occupied=occupied

lockers=[]
lockers.append(locker(b'\x9c\x9c\x1f\xc7\xbf\x78', False))

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Picking Up or Dropping Off?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Pick Up",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Drop Off",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):
    def cb(self, object):
        self.entry.delete(0,'end')
        self.entry.insert(0,pad.output)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Pickup Code", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(13, GPIO.IN)
        #GPIO.setup(20, GPIO.IN)
        #GPIO.setup(21, GPIO.IN)
        #GPIO.add_event_detect(16, GPIO.RISING, callback=self.cb)  
        #GPIO.add_event_detect(20, GPIO.RISING, callback=self.cb) 
        GPIO.add_event_detect(13, GPIO.RISING, callback=self.cb) 
        button4=tk.Button(self, text="Enter Code", command=lambda: unassign_locker(self.entry.get(), lockers))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", command=self.entry.delete(0, "end"))
        button2.pack()
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



class PageTwo(tk.Frame):
    def cb(self):
        self.entry.insert(0,pad.output)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Dropoff Code", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        button3=tk.Button(self, text="Update", command=self.cb)
        button3.pack()
        button4=tk.Button(self, text="Enter Code", command=lambda: assign_locker(self.entry.get(), lockers))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", command=self.entry.delete(0, "end"))
        button2.pack()
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


        
        


app = SeaofBTCapp()
app.mainloop()