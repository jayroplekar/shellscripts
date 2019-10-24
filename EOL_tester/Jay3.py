import Tkinter
import string, os, traceback
import tkFileDialog, tkFont, re
import time, threading, random, Queue

root = Tkinter.Tk()
helv16 = tkFont.Font(family="Helvetica", size=16, weight="bold")

def StartTest():

    #Query Engine Serial number and Test spec
    #Decide the Variant of the voltage specs to use based on test spec
    #Perform DAQ Check

    #Append Results to Errorlog
    print "Starting DAQ"

    #Query COMET for Any Errors
    print " Connecting with the ECM"

    #If Status is OK proceed to provide starter power via SCPI commands

    #Review time vs. rpm signal

    #Decide if Pass or Fail


def AbortTest():
    print "Aborting Test"

class GuiPart:

    def __init__(self, master, queue, endCommand):
        self.queue = queue
        root.title('Proto Tester')
        self.init_vars()

        # -- Create the menu frame, and menus to the menu frame
        menu_frame = Tkinter.Frame(root, height=50)
        menu_frame.pack(side=Tkinter.TOP)
        # menu_frame.pack(fill=Tkinter.X, side=Tkinter.TOP)
        menu_frame.tk_menuBar(self.topmenu(menu_frame, endCommand))

        self.Status_frame = self.StatusBar(root)
        self.Status_frame.seterr("in the main")

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                # print msg
                output_line = "Test Status \n" + str(msg)
                self.Status_frame.setmsg(output_line)
            except Queue.Empty:
                pass

    def GetSource(self):
        global fp
        fp = tkFileDialog.askopenfile()

    def topmenu(self, master, endCommand):
        file_btn = Tkinter.Menubutton(master, text='Manage Application', font=helv16)
        file_btn.pack(side=Tkinter.LEFT, padx="2m")
        file_btn.menu = Tkinter.Menu(file_btn)
        file_btn.menu.add_command(label="Open", underline=0, command=self.GetSource)
        file_btn.menu.add_command(label='Exit', underline=0, command=endCommand)
        file_btn['menu'] = file_btn.menu

        action_btn = Tkinter.Button(master, text='Start \n Test', font=helv16, command=StartTest)
        action_btn.pack(side=Tkinter.LEFT, padx="2m")

        print_btn = Tkinter.Button(master, text='Abort \n Test', font=helv16, command=AbortTest)
        print_btn.pack(side=Tkinter.LEFT, padx="2m")


        help_btn = Tkinter.Menubutton(master, text='Help!')
        help_btn.pack(side=Tkinter.RIGHT, padx="2m")
        help_btn.menu = Tkinter.Menu(help_btn)
        help_btn['menu'] = help_btn.menu

    def init_vars(self):
        global str1, str2, str3, strlist
        global raw_output, save_output, filter
        strlist = []
        for i in range(3): strlist.append(Tkinter.StringVar())
        str1 = Tkinter.StringVar()
        str2 = Tkinter.StringVar()
        str3 = Tkinter.StringVar()
        raw_output = Tkinter.IntVar()
        save_output = Tkinter.IntVar()
        filter = Tkinter.StringVar()
        save_output.set(1)
        filter.set("None")

    class StatusBar:
        def __init__(self, master):
            self.label = Tkinter.Label(master, text="", \
                                       bd=1, relief=Tkinter.SUNKEN, font=("Helvetica", "14"))
            self.label.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

        def setmsg(self, input):
            self.label.config(text=input, fg="blue")
            self.label.update_idletasks()

        def seterr(self, input):
            self.label.config(text=input, fg="red")
            self.label.update_idletasks()

        def clear(self):
            self.label.config(text="")
            self.label.update_idletasks()

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
    	self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 500 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(500, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(5)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0


rand = random.Random()

client = ThreadedClient(root)
root.mainloop()