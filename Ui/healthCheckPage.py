from tkinter import *
import tkinter as tk
from Ui import showGif as sg
from UiController import healthCheckPageController as hc
from Ui import overViewButtons as ovb
from Ui import logInPage as lip
import config as c
import threading
import time

FONT_HEALTH = c.APP['FONT_HEALTH']
FONT_OUTPUT = c.APP['FONT_OUTPUT']
FONT_MSG = ("Impact", 12, "underline")


class HealthCheckPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='black')
        self.v_img = PhotoImage(file='.\PicUi\\v.png')
        self.x_img = PhotoImage(file='.\PicUi\\x.png')
        self.img = PhotoImage(file='.\PicUi\\healthPic1.png')
        self.vv_img = PhotoImage(file='.\PicUi\\vv.png')
        self.xx_img = PhotoImage(file='.\PicUi\\xx.png')
        self.logout_img = PhotoImage(file='.\PicUi\\logout.png')
        self.send_img = PhotoImage(file='.\PicUi\\send.png')
        self.invalid = None
        self.pb = None
        self.input_txt = None
        self.health_controller = hc.HealthCheckPageController()
        self.background()
        self.logout, self.send = None, None
        self.input_output(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=110, y=75)

    def buttons(self):
        """
        Init buttons.
        :return logout: logout button
        :return send: send button
        """
        logout = tk.Button(self, image=self.logout_img, borderwidth=0, background='black',
                           command=lambda: self.logout_button())
        send = tk.Button(self, image=self.send_img, borderwidth=0, background='black',
                         command=lambda: self.send_button())
        send.place(bordermode=OUTSIDE, x=115, y=420)
        logout.place(bordermode=OUTSIDE, x=115, y=470)
        return logout, send

    def input_output(self, controller):
        """
        Init input output.
        """
        x = threading.Thread(target=lambda: self.show_components(controller))
        x.setDaemon(True)
        x.start()
        self.pb = sg.ShowGif(self)
        self.pb.config(bg='black')
        self.pb.show('.\\PicUi\\64x64.gif')
        self.pb.place(x=183, y=435)

    def show_components(self, controller):
        """
        show all health components in nice order.
        :param controller: gives the ability to switch between pages
        """
        x = 50
        y = 150
        i = 0
        colors = ['blue', 'green', 'red', 'orange', 'black', 'grey']
        map = self.health_controller.get_health_map()
        for key in map.keys():
            label = tk.Label(self, text=key, fg=colors[i % 6], font=FONT_HEALTH, bg='white')
            label.place(bordermode=OUTSIDE, x=x, y=y)
            y += 35
            i += 1
        y = 150
        i = 0
        for val in map.values():
            time.sleep(0.5)
            label = tk.Label(self, image=self.v_img, borderwidth=0) if val else \
                tk.Label(self, image=self.x_img, borderwidth=0)
            label.place(bordermode=OUTSIDE, x=x + 280, y=y + 5)
            y += 35
            i += 1
        self.pb.destroy()
        if self.health_controller.is_ready():
            tk.Label(self, image=self.vv_img, borderwidth=0).place(x=180, y=435)
            time.sleep(1)
            controller.manage_frame(lip.LogInPage)
        else:
            tk.Label(self, image=self.xx_img, borderwidth=0).place(x=180, y=435)
            time.sleep(2)
            self.failed_in_health_check()

    def failed_in_health_check(self):
        """
        in case of failure give the student an opportunity to send us
        en email.
        """
        fail_frame = Frame(self, width=390, height=430, background='black')
        fail_frame.place(x=20, y=93)
        self.logout, self.send = self.buttons()
        msg = tk.Label(self, text='If you think that we have a problem in our side,'
                                  '\nplease send a message via the text box below.'
                                  , bg='black', bd=0, fg='yellow', font=FONT_MSG)
        msg.place(bordermode=OUTSIDE, x=65, y=140)
        self.input_txt = tk.Text(self, height=13, width=33)
        self.input_txt.place(x=80, y=195)

    @staticmethod
    def logout_button():
        """
        if the student press on logout, send request to the controller
        in order to logout.
        """
        hc.close_application()

    def send_button(self):
        """
        if the student press on send, send request to the controller
        in order to send us en email.
        """
        hc.send_email(self.input_txt.get(1.0, "end-1c"))
