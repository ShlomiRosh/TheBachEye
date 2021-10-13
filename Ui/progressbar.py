from tkinter import ttk


def progressbar(self):
    """
    Create a progress bar with style.
    :param self: parent frame
    """
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("bar.Horizontal.TProgressbar", troughcolor='black', bordercolor='yellow',
                    background='blue', lightcolor='green', darkcolor='green')
    pb = ttk.Progressbar(self, style="bar.Horizontal.TProgressbar",
                         orient='horizontal', mode='indeterminate')
    return pb
