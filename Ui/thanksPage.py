from tkinter import *
import tkinter as tk
from UiController import thanksPageController as tpc
import config as c
import time
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']
FONT_MSG = c.APP['FONT_HEALTH']
SHOW_MSG_TIME = 10


class TanksPage(tk.Frame):
    """
    This class is responsible for displaying the Tanks Page.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.img = PhotoImage(file='.\PicUi\\tanks_background.png')
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.background()

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        x = threading.Thread(target=self.handle_time)
        x.setDaemon(True)
        x.start()

    def handle_time(self):
        """
        Show msg time.
        """
        hour, minute = tpc.get_time_remaining()
        if self.handle_late_student(hour):
            return
        self.handle_earliness_student(hour, minute)

    def handle_late_student(self, hour):
        if hour == 'V':
            label = tk.Label(self, text='You are going to enter the lesson.'
                             , bg='black', bd=0, fg='blue', font=FONT_MSG)
            label.place(bordermode=OUTSIDE, x=50, y=420)
            time.sleep(SHOW_MSG_TIME)
            tpc.successes()
            return True
        if hour == 'X':
            label = tk.Label(self, text='No lesson currently taking place\n(probably you are late).'
                             , bg='red', bd=0, fg='black', font=FONT_MSG)
            label.place(bordermode=OUTSIDE, x=40, y=420)
            time.sleep(SHOW_MSG_TIME)
            tpc.kill_program()

    def handle_earliness_student(self, hour, minute):
        self.hour.set(hour)
        self.minute.set(minute)
        self.second.set('00')
        label = tk.Label(self, text='The lesson will begin in:'
                         , bg='black', bd=0, fg='green', font=FONT_MSG)
        label.place(bordermode=OUTSIDE, x=60, y=420)
        hour_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.hour)
        hour_entry.place(x=60, y=470)
        minute_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.minute)
        minute_entry.place(x=110, y=470)
        second_entry = Entry(self, width=3, font=("Arial", 18, ""), textvariable=self.second)
        second_entry.place(x=160, y=470)
        self.time_logic()
        tpc.successes()

    def time_logic(self):
        """
        this function calculate the time left & updates the view.
        """
        temp = int(self.hour.get()) * 3600 + int(self.minute.get()) * 60 + int(self.second.get())
        while temp > -1:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            # using format () method to store the value up to
            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))
            # updating the GUI window after decrementing the temp value every time
            self.update()
            time.sleep(1)
            temp -= 1
