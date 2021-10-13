import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
from Services import loggerService as ls


class ShowGif(tk.Label):

    def __init__(self, frame):
        """
        initialize parameters & super class
        :param frame: the frame in which the gif will be shown
        """
        super().__init__(frame)
        self.frames = None
        self.delay = None

    def show(self, root):
        """
        load the gif as images
        :param:root: a PIL Image instance or a string filename
        """
        if isinstance(root, str):
            root = Image.open(root)
        frames_img = []
        try:
            for i in count(1):
                frames_img.append(ImageTk.PhotoImage(root.copy()))
                root.seek(i)
        except EOFError as e:
            pass
            # TODO: uncomment this line in final version
            # ls.get_logger().error(f'failed to load the picture, due to: {str(e)}')
        self.frames = cycle(frames_img)
        try:
            self.delay = root.info['duration']
        except:
            self.delay = 100
        if len(frames_img) == 1:
            self.config(image=next(self.frames))
        else:
            self.show_next_frame()

    def stop(self):
        """
        close the animation gif
        """
        self.config(image=None)
        self.frames = None

    def show_next_frame(self):
        """
        load the next frame after the amount of time passed
        """
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.show_next_frame)


def for_tests_only():
    """
    this function is used only for tests.
    """
    root = tk.Tk()
    panel = tk.Frame(root)
    panel.pack(expand=tk.YES, fill=tk.BOTH)
    lbl = ShowGif(panel)
    lbl.place(bordermode='outside', x=135, y=500)
    lbl.show('..\\PicUi\\100x100.gif')
    root.mainloop()


if __name__ == "__main__":
    for_tests_only()
