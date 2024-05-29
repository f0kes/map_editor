import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD


class ImagePreview:
    def __init__(self, placeholder):
        self.current_box = None
        self.panel = ttk.Frame(placeholder)
        self.frame = ttk.Frame(self.panel, borderwidth=5, relief="ridge", width=128, height=128)
        self.frame2 = ttk.Frame(self.panel, borderwidth=5, relief="ridge", width=128, height=128)
        # first column image, second column empty, third column image
        self.image1 = ttk.Label(self.frame, text='Original')
        self.image2 = ttk.Label(self.frame2, text='Replacement', image=None)

        self.image2.drop_target_register(DND_FILES)
        self.image2.dnd_bind('<<Drop>>', self.drop_callback)

        self.empty = ttk.Label(self.panel)
        self.blank = Image.new('RGB', (128, 128), (255, 255, 255))

        self.set_image1(self.blank)
        self.set_image2(self.blank)

    def grid(self, **kw):
        self.panel.grid(**kw)
        self.frame.grid(row=0, column=0, columnspan=1, pady=10, padx=30, sticky='nw')
        self.frame2.grid(row=0, column=2, columnspan=1, pady=10, padx=10, sticky='nw')
        self.image1.grid(row=0, column=0)
        self.image2.grid(row=0, column=0)

    def set_current_box(self, box):
        self.current_box = box
        self.blit()

    def set_image1(self, image: Image.Image):
        image = image.resize((128, 128))
        image = ImageTk.PhotoImage(image)
        self.image1.configure(image=image)
        self.image1.image = image

    def set_image2(self, image: Image.Image):
        image = image.resize((128, 128))
        image = ImageTk.PhotoImage(image)
        self.image2.configure(image=image)
        self.image2.image = image

    def drop_callback(self, event):
        file_path = event.data
        image = Image.open(file_path)
        self.current_box.set_replacement_image(image)
        self.blit()

    def blit(self):
        box = self.current_box
        original = box.initial_images[0]
        replacement = box.replacement_image
        if original is not None:
            self.set_image1(original)
        else:
            self.set_image1(self.blank)
        if replacement is not None:
            self.set_image2(replacement)
        else:
            self.set_image2(self.blank)
