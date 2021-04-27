import tkinter as tk
from keypad_helper import KeyPadHelper as keypadhelper
from locker_communication import open_locker
from locker_communication import assign_locker
from locker_communication import unassign_locker
import RPi.GPIO as GPIO 
from locker_communication import setup
import threading
from locker_communication import stop_setup
from security import main
from locker_communication import restore
from locker_communication import open_all_lockers

LARGE_FONT= ("Verdana", 12)
#GPIO.setmode(GPIO.BOARD)
pin0=0
pin1=1
pin2=2
pin3=3


pad=keypadhelper()
address=0000

check_keypad=False

restore()
#lockers.append(locker(b'\x9c\x9c\x1f\xc7\xbf\x78', False))

def start_setup(popup):
    global setup_mode
    setup_mode=True
    lockers=setup()
    popup.set(str(len(lockers))+" lockers set up")
    print(popup.get())
    return

def start_camera():
    run_camera=False
    if(run_camera):
        main()

def start_keypad(var):
    global check_keypad
    while(check_keypad):
        if(var.get()!=pad.output):
            try:
                var.insert('end',pad.output[len(pad.output)-1])
            except:
                placeholder=1


y=threading.Thread(name='Security', target=main, daemon=True)
y.start()

def setup_helper(popup):
    popup.set("Setup mode initiated")
    x = threading.Thread(name='Setup', target=start_setup, args=(popup,), daemon=True)
    x.start()

def admin_check(code, popup, controller):
    pad.reset_output()
    admin_code=1111
    #x = threading.Thread(target=start_setup, args=(popup,), daemon=True)
    print("Admin Check Runs")
    if(str(admin_code)==code.get()):
        #x.start()
        popup.set("Code is correct")
        print(popup.get())
        print("After popup is set")
    else:
        popup.set("Code is incorrect. Try again.")
    code.delete(0,'end')
    controller.show_frame(Admin_Control)
    

def unassign_locker_helper(pickup_code, popup):
    pad.reset_output()
    status, number, locker_unassigned=unassign_locker(pickup_code.get())
    pickup_code.delete(0,'end')
    if(status==True):
        popup.set("Code is Correct. Locker "+ str(number)+ " has opened!")
    elif(status==False):
        popup.set("Code is incorrect. Try again")
    elif(locker_unassigned==False):
        popup.set("You do not currently have packages to pick up")

def assign_locker_helper(deposit_code, popup):
    pad.reset_output()
    status, number, locker_assigned=assign_locker(deposit_code.get())
    deposit_code.delete(0,'end')
    if(status==True and locker_assigned==True):
        popup.set("Code is Correct. Locker "+ str(number)+ " has opened!")
    elif(status==False):
        popup.set("Code is incorrect. Try again")
    elif(locker_assigned==False):
        popup.set("No lockers available")

class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen',False)
        container = tk.Frame(self, bg='blue')

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, AdminPage, Admin_Control):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.configure(bg='#49657b')
        frame.tkraise()
    

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global check_keypad
        check_keypad=False
        tk.Frame.__init__(self,parent)
        self.configure(bg='#49657b')
        label = tk.Label(self, text="Picking Up or Dropping Off?", font='Lato 18 bold', bg='#49657b')
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Pick Up", height=2, width=10, bg='#708090',
                            command=lambda: controller.show_frame(PageOne))
        button.pack(pady=10, padx=10)

        button2 = tk.Button(self, text="Drop Off", height=2, width=10, bg='#708090',
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10, padx=10)
        button3=tk.Button(self,text="Admin Page", height=2, width=10, bg='#708090', command=lambda: controller.show_frame(AdminPage))
        button3.pack(pady=10, padx=10)

class PageOne(tk.Frame):
    def delete_entry(self):
        self.page1entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        #self.configure(bg='#49657b')
        global check_keypad
        check_keypad=True
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Pickup Code", font=LARGE_FONT, bg='#49657b')
        label.pack(pady=10,padx=10)
        label.pack(pady=10,padx=10)
        self.page1entry=tk.Entry(self)
        self.page1entry.pack(pady=10, padx=10)
        z=threading.Thread(name='keypad1', target=start_keypad, args=(self.page1entry,),daemon=True)
        z.start()
        popup=tk.StringVar()
        popup.set("")
        message=tk.Label(self, textvariable=popup)
        print("Code to Function " +self.page1entry.get())
        button4=tk.Button(self, text="Enter Code", height=2, width=10, bg='#708090', command=lambda: unassign_locker_helper(self.page1entry, popup))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", height=2, width=10,  bg='#708090', command=self.delete_entry)
        button2.pack()
        button1 = tk.Button(self, text="Back to Home", height=2, width=10,  bg='#708090',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        message.pack()




class PageTwo(tk.Frame):
    def delete_entry(self):
        self.entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        global check_keypad
        check_keypad=True
        #self.configure(bg='#49657b')
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Dropoff Code", font=LARGE_FONT, bg='#49657b')
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        z=threading.Thread(name='keypad2', target=start_keypad, args=(self.entry,),daemon=True)
        z.start()
        popup=tk.StringVar()
        popup.set("")
        message=tk.Label(self, textvariable=popup)
        button4=tk.Button(self, text="Enter Code", height=2, width=10,  bg='#708090', command=lambda: assign_locker_helper(self.entry, popup))
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", height=2, width=10,  bg='#708090', command=self.delete_entry)
        button2.pack()
        button1 = tk.Button(self, text="Back to Home", height=2, width=10,  bg='#708090',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        message.pack()

class AdminPage(tk.Frame):
    def delete_entry(self):
        self.entry.delete(0,'end')
        pad.reset_output()
    def __init__(self, parent, controller):
        global check_keypad
        check_keypad=True
        #self.configure(bg='#49657b')
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter Admin Password", font=LARGE_FONT, bg='#49657b')
        label.pack(pady=10,padx=10)
        self.entry=tk.Entry(self)
        self.entry.pack(pady=10, padx=10)
        z=threading.Thread(name='keypad3',target=start_keypad, args=(self.entry,),daemon=True)
        z.start()
        popup=tk.StringVar()
        popup.set("")
        message=tk.Label(self, textvariable=popup)
        button4=tk.Button(self, text="Enter Code", command=lambda: admin_check(self.entry, popup, controller), height=2, width=10, bg='#708090')
        button4.pack()
        button2 = tk.Button(self, text="Retype Code", height=2, width=10,  bg='#708090', command=self.delete_entry)
        button2.pack()
        button1 = tk.Button(self, text="Back to Home", height=2, width=10,  bg='#708090',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        message.pack()

class Admin_Control(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Admin Control Page", font=LARGE_FONT, bg='#49657b')
        label.pack(pady=10,padx=10)
        popup=tk.StringVar()
        popup.set("")
        message=tk.Label(self, textvariable=popup)
        button1= tk.Button(self,text="Start Setup Mode", height=2, width=10,  bg='#708090', command=lambda: setup_helper(popup))
        button1.pack(padx=10, pady=10)
        button2=tk.Button(self,text="End Setup Mode", height=2, width=10,  bg='#708090', command=stop_setup)
        button2.pack(padx=10, pady=10)
        button3=tk.Button(self, text="Open All Lockers", height=2, width=10,  bg='#708090', command=open_all_lockers)
        button3.pack(padx=10, pady=10)
        button4 = tk.Button(self, text="Back to Home", height=2, width=10,  bg='#708090',
                            command=lambda: controller.show_frame(StartPage))
        button4.pack(padx=10, pady=10)
        message.pack()
        
        
        


app = SeaofBTCapp()
app.mainloop()
