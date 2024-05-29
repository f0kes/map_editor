import tkinter as tk
from tkinter import ttk

import app_setting
from file_selector import FileSelector
from image_preview import ImagePreview


class WorkPanel:
    def __init__(self, placeholder, width, app_settings: app_setting.AppSettings):
        self.panel = ttk.Frame(placeholder)

        # self.file_selector = FileSelector(self.panel, app_settings)
        # self.file_selector.grid(row=3, column=0)

        self.image_frame = ttk.Frame(self.panel)
        self.image_frame.grid(row=0, column=0)

        self.input_frame = ttk.Frame(self.panel)
        self.input_frame.grid(row=1, column=0, sticky='s')

        self.box_buttons_frame = ttk.Frame(self.panel)
        self.box_buttons_frame.grid(row=2, column=0, sticky='s')

        self.files_frame = ttk.Frame(self.panel)
        self.files_frame.grid(row=3, column=0, sticky='s')

        self.delete_button = ttk.Button(self.box_buttons_frame, text='Delete', command=app_settings.delete_current_box)
        self.delete_button.grid(row=0, column=1, sticky='s')
        self.export_original_button = ttk.Button(self.box_buttons_frame, text='Export Original',
                                                 command=app_settings.export_original)
        self.export_original_button.grid(row=0, column=0, sticky='s')

        self.popup_button = ttk.Button(self.files_frame, text='File Select', command=self.file_selector_open)
        self.popup_button.grid(row=0, column=0, sticky='s', padx=10, pady=10)

        self.save = ttk.Button(self.files_frame, text='Save', command=self.save_callback)
        self.save.grid(row=0, column=1, sticky='s', pady=10)

        self.app_settings = app_settings
        vcmd = (self.panel.register(self.validate_callback))
        self.select_x_res_var = tk.IntVar()
        self.select_y_res_var = tk.IntVar()

        self.res_x_entry = ttk.Entry(self.input_frame, textvariable=self.select_x_res_var, width=10, validate='all',
                                     validatecommand=(vcmd, '%P'))
        self.res_y_entry = ttk.Entry(self.input_frame, textvariable=self.select_y_res_var, width=10, validate='all',
                                     validatecommand=(vcmd, '%P'))
        self.select_x_res_var.trace("w", lambda name, index, mode, sv=self.select_x_res_var: self.update_res_x(sv))
        self.select_y_res_var.trace("w", lambda name, index, mode, sv=self.select_y_res_var: self.update_res_y(sv))
        self.select_x_res_var.set(768)
        self.select_y_res_var.set(768)

        self.image_preview = ImagePreview(self.image_frame)
        self.app_settings.add_box_selected_callback(self.on_box_selected)

    def file_selector_open(self):
        popup = tk.Toplevel()
        popup.grab_set()
        popup.title("File Selector")
        popup.attributes('-topmost', 'true')
        selector = FileSelector(popup, self.app_settings)
        selector.grid(sticky='n', pady=10, padx=10)
        popup.columnconfigure(0, weight=1)
        popup.rowconfigure(0, weight=1)

    def grid(self, **kw):
        self.panel.grid(**kw)
        self.res_x_entry.grid(row=0, column=0, pady=10, padx=10, sticky='s')
        self.res_y_entry.grid(row=0, column=1, pady=10, padx=10, sticky='s')
        self.image_preview.grid(row=0, column=0)

    def validate_callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def update_res_x(self, x):
        self.app_settings.set_x_size(x.get())

    def update_res_y(self, y):
        self.app_settings.set_y_size(y.get())

    def on_box_selected(self, box):
        self.image_preview.set_current_box(box)

    def save_callback(self):
        self.app_settings.save_image()
