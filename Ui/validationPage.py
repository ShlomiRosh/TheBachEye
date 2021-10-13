from tkinter import *
import tkinter as tk
from UiController import validationController as vc
from Ui import overViewButtons as ovb
from Ui import uploadPicPage as up
from Ui import showGif as sg
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']


class ValidationPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='black')
        self.email_img = PhotoImage(file='.\PicUi\\send.png')
        self.check_img = PhotoImage(file='.\PicUi\\check_pic.png')
        self.img = PhotoImage(file='.\PicUi\\valid.png')
        self.img1 = PhotoImage(file='.\PicUi\\valid1.png')
        self.email = ''
        self.count_flg = 0
        self.button_flg = 0
        self.invalid_email = None
        self.invalid_code = None
        self.pb = None
        self.validation_controller = vc.ValidationController()
        self.bg = self.background()
        self.email_l, self.code_l, self.entry = self.input_output()
        self.email_b, self.check_b = self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=110, y=75)
        return panel

    def input_output(self):
        """
        Init input output.
        """
        email_l = tk.Label(self, text='Please enter your email', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        email_l.place(bordermode=OUTSIDE, x=110, y=190)
        entry = Entry(self)
        entry.place(bordermode=OUTSIDE, x=110, y=215, width=220, height=40)
        code_l = tk.Label(self, text='Please enter the validation code', bg='black', bd=0, fg='yellow',
                          font=FONT_OUTPUT)
        return email_l, code_l, entry

    def buttons(self, controller):
        """
        Init buttons.
        :param controller: gives the ability to switch between pages
        """
        email_b = tk.Button(self, image=self.email_img, borderwidth=0, background='black',
                            command=lambda: self.email_button(controller))
        email_b.place(bordermode=OUTSIDE, x=118, y=460)
        check_b = tk.Button(self, image=self.check_img, borderwidth=0, background='black',
                            command=lambda: self.check_button(controller))
        return email_b, check_b

    def email_button(self, controller):
        """
        what to do if the user presses the email button
        :param controller: gives the ability to switch between pages
        """
        check_email = self.validation_controller.check_email(self.entry.get())
        if check_email != 'OK':
            self.invalid_email = ovb.create_msg(self, 260, 255, check_email)
        else:
            self.email = self.entry.get()
            self.bg.configure(image=self.img1)
            self.bg.image = self.img1
            self.pb = sg.ShowGif(self)
            self.pb.config(bg='black')
            self.pb.show('.\\PicUi\\100x100.gif')
            self.pb.place(x=160, y=360)
            x = threading.Thread(target=lambda: self.send_validation_code())
            x.setDaemon(True)
            x.start()

    def check_button(self, controller):
        """
        after the email validation send & the student enter the
        validation code, handle this logic.
        :param controller: gives the ability to switch between pages
        """
        check_code = self.validation_controller.check_code(self.entry.get())
        if check_code != 'OK':
            self.invalid_email = ovb.create_msg(self, 260, 255, check_code)
            self.count_flg += 1
            if self.count_flg >= 3:
                self.code_l.place_forget()
                self.entry.delete(0, 'end')
                self.email_l.place(bordermode=OUTSIDE, x=110, y=190)
                self.check_b.place_forget()
                self.email_b.place(bordermode=OUTSIDE, x=118, y=460)
                self.clean_entries()
                self.invalid_email = ovb.create_msg(self, 260, 255, 'To many attempts\nEnter email again.')
        else:
            self.validation_controller.send_email_to_server(self.email)
            controller.manage_frame(up.UploadPicPage)

    def send_validation_code(self):
        """
        this function will send the email im different thread.
        """
        is_sent = self.validation_controller.send_validation_email(self.email)
        self.pb.stop()
        self.pb.destroy()
        if is_sent:
            self.email_l.place_forget()
            self.entry.delete(0, 'end')
            self.code_l.place(bordermode=OUTSIDE, x=110, y=190)
            self.email_b.place_forget()
            self.check_b.place(bordermode=OUTSIDE, x=118, y=460)
            self.count_flg = 0
            self.clean_entries()
            self.bg.configure(image=self.img)
            self.bg.image = self.img
        else:
            self.invalid_email = ovb.create_msg(self, 260, 255, 'Please try anther email.')

    def clean_entries(self):
        """
        cleaning the page entries.
        """
        if self.invalid_email is not None:
            self.invalid_email.destroy()
        if self.invalid_code is not None:
            self.invalid_code.destroy()
