from tkinter import Frame


class BaseView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def configure_grid(frame, cols, rows):
        for i in range(cols):
            frame.columnconfigure(i, weight=1)

        for i in range(rows):
            frame.rowconfigure(i, weight=1)
