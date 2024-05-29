# -*- coding: utf-8 -*-
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.

# -*- coding: utf-8 -*-
# Advanced zoom for images of various types from small to huge up to several GB
import tkinter as tk
import warnings

from tkinter import ttk
from PIL import Image
import app_setting
import image_cutter
from image_canvas import CanvasImage
from work_panel import WorkPanel
from tkinterdnd2 import DND_FILES, TkinterDnD


class MainWindow(ttk.Frame):
    """ Main window class """

    def __init__(self, mainframe: tk.Tk, app_settings: app_setting.AppSettings, image):
        """ Initialize the main Frame """
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('GigaTile')
        self.master.geometry('1280x720')  # size of the main window
        self.master.rowconfigure(0, weight=3)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)
        canvas = CanvasImage(self.master, app_settings, image)  # create widget
        work_panel = WorkPanel(self.master, 0, app_settings)
        canvas.grid(row=0, column=0)  # show widget
        work_panel.grid(row=0, column=1)


if __name__ == '__main__':
    Image.MAX_IMAGE_PIXELS = 1000000000  # suppress DecompressionBombError for the big image
    # path = '/var/home/f0kes/Pictures/map_12k.png'
    with warnings.catch_warnings():  # suppress DecompressionBombWarning
        warnings.simplefilter('ignore')
        # create EMPTY image
        image = Image.new('RGB', (100, 100), (0, 0, 0))
    cutter = image_cutter.ImageCutter([image])
    app_settings = app_setting.AppSettings(image, cutter)
    app = MainWindow(TkinterDnD.Tk(), app_settings=app_settings, image=image)

    app.mainloop()
