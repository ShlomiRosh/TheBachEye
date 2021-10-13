import os
from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from UiController import takePicPageController as tp
from Ui import overViewButtons as ovb
from Ui import thanksPage
from Ui import progressbar
import config as c
import threading

FONT_OUTPUT = c.APP['FONT_OUTPUT']
FONT_MSG = c.APP['FONT_MSG']


class TakePicPage(tk.Frame):
    """
    This class is responsible for displaying the Take Pic Page.
    """
    def __init__(self, parent, controller):
        """
        Init variables and calling functions.
        :param parent: the parent frame
        :param controller: gives the ability to switch between pages
        """
        tk.Frame.__init__(self, parent)
        self.take_pic_img = PhotoImage(file='.\PicUi\\take_pic.png')
        self.check_img = PhotoImage(file='.\PicUi\\check_pic.png')
        self.img = PhotoImage(file='.\PicUi\\take_pic_background.png')
        self.face_recognition_fail = None
        self.pb = None
        self.background()
        # capture video frames.
        self.vs = cv2.VideoCapture(c.CAM_SRC, cv2.CAP_DSHOW)
        # store output path.
        self.output_path = "./PicUi/"
        self.file_name = "student_snapshot.jpg"
        # current image from the camera.
        self.current_image = None
        # initialize image panel.
        self.panel_image = None
        self.panel = tk.Label(self)
        self.panel.place(bordermode=OUTSIDE, x=40, y=125, height=350, width=350)
        self.check_button = None
        self.take_button = None
        self.buttons(controller)

    def background(self):
        """
        Init background.
        """
        panel = tk.Label(self, image=self.img)
        panel.pack(expand=tk.YES, fill=tk.BOTH)
        pure_sarcasm = tk.Label(self, text='A system for helping and improving learning!'
                                , bg='black', bd=0, fg='green', font=FONT_OUTPUT)
        pure_sarcasm.place(bordermode=OUTSIDE, x=135, y=85)
        note = tk.Label(self, text='Note here!', bg='black', bd=0, fg='blue', font=FONT_MSG)
        note.place(bordermode=OUTSIDE, x=40, y=105)
        msg = 'For our face recognition system you need to\n''to take a snapshot of your face\n''' \
              'at a good light.'
        ovb.create_tool_tip(note, text=msg)

    def buttons(self, controller):
        """
        Init buttons & start video loop.
        :param controller: gives the ability to switch between pages
        """
        self.take_button = tk.Button(self, image=self.take_pic_img, borderwidth=0, background='black',
                                     command=lambda: self.take_snapshot(controller))
        self.take_button.place(bordermode=OUTSIDE, x=118, y=490)
        self.check_button = tk.Button(self, image=self.check_img, borderwidth=0, background='black',
                                      command=lambda: self.check_image_recognition(controller))
        # Start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame.
        self.video_loop()

    def video_loop(self):
        """
        Get frame from the video stream and show it in Tkinter.
        """
        ok, frame = self.vs.read()
        if ok:
            # Convert colors from BGR to RGBA.
            cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # Convert image for PIL.
            self.current_image = Image.fromarray(cv2_image)
            # Convert image for tkinter.
            img_tk = ImageTk.PhotoImage(image=self.current_image)
            # Anchor img_tk so it does not be deleted by garbage-collector.
            self.panel.img_tk = img_tk
            # Show the image.
            self.panel.config(image=img_tk)
        # Call the same function after 30 milliseconds.
        self.after(30, self.video_loop)

    def take_snapshot(self, controller):
        """
        Take snapshot & save it.
        """
        self.clean_entries()
        # Take snapshot and save it to the file.
        p = os.path.join(self.output_path, self.file_name)
        self.current_image = self.current_image.convert('RGB')
        # Save image as jpeg file.
        self.current_image.save(p, "JPEG")
        self.show_image()

    def show_image(self):
        """
        Show user the image that was taken.
        """
        self.take_button.place_forget()
        self.check_button.place(bordermode=OUTSIDE, x=118, y=490)
        img = Image.open(self.output_path + self.file_name)
        # Resize the image and apply a high-quality down sampling filter.
        img = img.resize((300, 300), Image.ANTIALIAS)
        # PhotoImage class is used to add image to widgets, icons etc.
        img = ImageTk.PhotoImage(img)
        if self.panel_image is not None:
            self.panel_image.destroy()
            self.panel_image = None
        self.panel_image = Label(self, image=img)
        # Set the image as img.
        self.panel_image.image = img
        self.panel_image.place(bordermode=OUTSIDE, x=40, y=125, height=350, width=350)

    def check_image_recognition(self, controller):
        """
        Start process to check student recognition.
        """
        self.pb = progressbar.progressbar(self)
        self.pb.place(bordermode=OUTSIDE, x=118, y=490, height=42, width=200)
        self.pb.start()
        x = threading.Thread(target=lambda: self.handle_recognition(controller))
        x.setDaemon(True)
        x.start()

    def handle_recognition(self, controller):
        """
        Check student recognition if it fail start again else go to next page.
        """
        if not tp.check_recognition(self.output_path + self.file_name):
            self.pb.destroy()
            self.check_button.place_forget()
            self.panel_image.place_forget()
            self.take_button.place(bordermode=OUTSIDE, x=118, y=490)
            msg = 'Your face recognition failed.\nPlease take anther snapshot\nIn better lighting conditions.'
            self.face_recognition_fail = ovb.create_msg(self, 118, 533, msg)
        else:
            self.destructor(controller)

    def clean_entries(self):
        """
        Clearing the page.
        """
        if self.face_recognition_fail is not None:
            self.face_recognition_fail.destroy()

    def destructor(self, controller):
        """
        Release cam stream & go to next page.
        """
        self.vs.release()
        cv2.destroyAllWindows()
        controller.manage_frame(thanksPage.TanksPage)
