from tkinter import *
import tkinter as tk
from Ui import progressbar
from UiController import logInPageController as lc
from Ui import overViewButtons as ovb
from Ui import takePicPage as tp
from Ui import validationPage as vp
from Ui import uploadPicPage as up
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']


class LogInPage(tk.Frame):
    """
    This class is responsible for displaying the start page.
    """
    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        self.login_img = PhotoImage(file='.\PicUi\\login_b.png')
        self.img = PhotoImage(file='.\PicUi\\login_background.png')
        self.invalid_password = None
        self.invalid_code = None
        self.pb = None
        # In these functions I will create & place all of the components
        # in the appropriate places, and run logic according to the user's requirements.
        self.background()
        self.password, self.class_code = self.input_output()
        self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='blue', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)

    def input_output(self):
        """
        Init input output.
        """
        password = tk.Label(self, text='Password:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        password.place(bordermode=OUTSIDE, x=110, y=210)
        e_password = Entry(self)
        e_password.place(bordermode=OUTSIDE, x=110, y=235, width=220, height=40)
        class_code = tk.Label(self, text='Class Code:', bg='black', bd=0, fg='yellow', font=FONT_OUTPUT)
        class_code.place(bordermode=OUTSIDE, x=110, y=295)
        e_class_code = Entry(self)
        e_class_code.place(bordermode=OUTSIDE, x=110, y=320, width=220, height=40)
        return e_password, e_class_code

    def buttons(self, controller):
        """
        Init buttons.
        :param controller: gives the ability to switch between pages
        """
        login = tk.Button(self, image=self.login_img, borderwidth=0, background='black',
                          command=lambda: self.login_button(controller))
        login.place(bordermode=OUTSIDE, x=118, y=470)

    def login_button(self, controller):
        """
        The logic that occurs when the user clicks login.
        :param controller: gives the ability to switch between pages
        """
        obg = lc.LoginController(self.password.get(), self.class_code.get())
        msg = obg.check_validation()
        if msg['Class Code'] != '':
            self.invalid_code = ovb.create_msg(self, 260, 360, msg['Class Code'])
        if msg['Password'] != '':
            self.invalid_password = ovb.create_msg(self, 260, 275, msg['Password'])
        if msg['Password'] == '' and msg['Class Code'] == '':
            self.pb = progressbar.progressbar(self)
            self.pb.place(bordermode=OUTSIDE, x=118, y=420, height=30, width=200)
            self.pb.start()
            x = threading.Thread(target=lambda: self.check_for_pic(controller, obg))
            x.setDaemon(True)
            x.start()

    def check_for_pic(self, controller, obg):
        """
        Check if the user is on the system and has an updated image on the server.
        :param controller: gives the ability to switch between pages
        :param obg: the login controller
        """
        student_data = obg.check_student_data_in_server()
        self.pb.destroy()
        self.clean_entries()
        if student_data['Class Code'] != '':
            self.invalid_code = ovb.create_msg(self, 260, 360, student_data['Class Code'])
        if student_data['Password'] != '':
            self.invalid_password = ovb.create_msg(self, 260, 275, student_data['Password'])
        if student_data['Class Code'] != '' or student_data['Password'] != '':
            return
        page_to_jump = obg.page_to_jump()
        if page_to_jump == 'ToValidation':
            controller.manage_frame(vp.ValidationPage)
        elif page_to_jump == 'ToUpload':
            controller.manage_frame(up.UploadPicPage)
        elif page_to_jump == 'ToSnapshot':
            controller.manage_frame(tp.TakePicPage)

    def clean_entries(self):
        """
        Clearing the page.
        """
        self.password.delete(0, 'end')
        self.class_code.delete(0, 'end')
        if self.invalid_password is not None:
            self.invalid_password.destroy()
        if self.invalid_code is not None:
            self.invalid_code.destroy()




