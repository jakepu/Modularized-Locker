import tkinter as tk
from keypad_helper import KeyPadHelper as keypadhelper
from locker_communication import open_locker
from locker_communication import assign_locker
from locker_communication import unassign_locker
import RPi.GPIO as GPIO 
from locker_communication import setup
import threading
from locker_communication import stop_setup

LARGE_FONT= ("Verdana", 12)
#GPIO.setmode(GPIO.BOARD)
pin0=0
pin1=1
pin2=2
pin3=3


pad=keypadhelper()
address=0000


#lockers.append(locker(b'\x9c\x9c\x1f\xc7\xbf\x78', False))

def start_setup(object):
    global setup_mode
    setup_mode=True
    setup()



x = threading.Thread(target=start_setup, args=(1,), daemon=True)

def admin_check(code):
    pad.reset_output()
    admin_code=1111
    if(str(admin_code)==code.get()):
        x.start()
    code.delete(0,'end')
    

def unassign_locker_helper(pickup_code):
    pad.reset_output()
    unassign_locker(pickup_code.get())
    pickup_code.delete(0,'end')

def assign_locker_helper(deposit_code):
    pad.reset_output()
    assign_locker(deposit_code.get())
    deposit_code.delete(0,'end')


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        #self.attributes('-fullscreen',True)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, AdminPage):

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
        button3=tk.Button(self,text="Admin Page", command=lambda: controller.show_frame(AdminPage))
        button3.pack()

class PageOne(tk.Frame):
    def cb(self):
        self.page1entry.insert(0,pad.output)
    def delete_entry(self):
        self.page1entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Pickup Code", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.page1entry=tk.Entry(self)
        self.page1entry.pack(pady=10, padx=10)
        print("Code to Function " +self.page1entry.get())
        button4=tk.Button(self, text="Enter Code", command=lambda: unassign_locker_helper(self.page1entry))
        button4.pack()
        button3=tk.Button(self, text="Show Entered Code", command=self.cb)
        button3.pack()
        button2 = tk.Button(self, text="Retype Code", command=self.delete_entry())
        button2.pack()
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



class PageTwo(tk.Frame):
    def cb(self):
        self.entry.insert(0,pad.output)
    def delete_entry(self):
        self.entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Dropoff Code", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        button3=tk.Button(self, text="Show Entered Code", command=self.cb)
        button3.pack()
        button4=tk.Button(self, text="Enter Code", command=lambda: assign_locker_helper(self.entry))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", command=self.delete_entry())
        button2.pack()
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class AdminPage(tk.Frame):
    def cb(self):
        self.entry.insert(0,pad.output)
    def delete_entry(self):
        self.entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Admin Password", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        button3=tk.Button(self, text="Show Entered Code", command=self.cb)
        button3.pack()
        button4=tk.Button(self, text="Enter Code", command=lambda: admin_check(self.entry))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", command=self.delete_entry())
        button2.pack()
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button5=tk.Button(self,text="End Setup Mode", command=stop_setup)
        button5.pack()

        
        
        


app = SeaofBTCapp()
app.mainloop()