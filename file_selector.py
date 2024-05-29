from tkinter import ttk, Listbox, filedialog

from app_setting import AppSettings


class FileSelector:
    def __init__(self, placeholder, app_settings: AppSettings):
        self.base_image_path_str = ''
        self.controlnets_paths = []

        self.app_settings = app_settings
        self.global_frame = ttk.Frame(placeholder)
        self.base_image_frame = ttk.Frame(self.global_frame, borderwidth=5, relief="ridge", padding=5)
        self.base_image_frame.grid(row=0, column=0)

        self.controlnets_frame = ttk.Frame(self.global_frame, borderwidth=5, relief="ridge", padding=5)
        self.controlnets_frame.grid(row=1, column=0)

        self.buttons_frame = ttk.Frame(self.global_frame)
        self.buttons_frame.grid(row=2, column=0)

        # base image frame contains a bordered frame with a file path label, and a button to select a file
        self.base_image_label = ttk.Label(self.base_image_frame, text='Base Image')
        self.base_image_label.grid(row=0, column=1, padx=5)
        self.base_image_path = ttk.Label(self.base_image_frame, text='No file selected', borderwidth=5, relief="ridge",
                                         padding=5)
        self.base_image_path.grid(row=1, column=0, padx=5)
        self.base_image_button = ttk.Button(self.base_image_frame, text='Select File', padding=5,
                                            command=self.select_base_callback)
        self.base_image_button.grid(row=1, column=2, padx=5)
        # controlnets frame contains a listbox of file paths of controlnets, and buttons to add and remove controlnets
        self.controlnets_label = ttk.Label(self.controlnets_frame, text='Controlnets')
        self.controlnets_label.grid(row=0, column=1, padx=5)
        self.controlnets_listbox = Listbox(self.controlnets_frame, height=5)
        self.controlnets_listbox.grid(row=1, column=0, padx=5)
        self.controlnets_add_button = ttk.Button(self.controlnets_frame, text='Add', padding=5,
                                                 command=self.add_controlnet_callback)
        self.controlnets_add_button.grid(row=1, column=1, padx=5)
        self.controlnets_remove_button = ttk.Button(self.controlnets_frame, text='Remove', padding=5,
                                                    command=self.remove_controlnet_callback)
        self.controlnets_remove_button.grid(row=1, column=2, padx=5)
        # button frame contains two buttons, OK and Cancel
        self.ok_button = ttk.Button(self.buttons_frame, text='OK', padding=5, command=self.ok_callback)
        self.ok_button.grid(row=0, column=0, padx=5)
        # self.cancel_button = ttk.Button(self.buttons_frame, text='Cancel', padding=5)
        # self.cancel_button.grid(row=0, column=1, padx=5)

    def grid(self, **kw):
        self.global_frame.grid(**kw)

    def select_base_callback(self):
        filetypes = (
            ('png', '*.png'),
        )
        path = filedialog.askopenfilename(
            title='Select a base image',
            filetypes=filetypes
        )
        path_end = path.split('/')[-1]
        self.base_image_path_str = path
        self.base_image_path.config(text=path_end)

    def add_controlnet_callback(self):
        filetypes = (
            ('png', '*.png'),
        )
        path = filedialog.askopenfilename(
            title='Select a controlnet image',
            filetypes=filetypes
        )
        path_end = path.split('/')[-1]
        self.controlnets_paths.append(path)
        self.controlnets_listbox.insert(self.controlnets_listbox.size(), path_end)

    def remove_controlnet_callback(self):
        for i in self.controlnets_listbox.curselection():
            self.controlnets_listbox.delete(i)
            self.controlnets_paths.pop(i)

    def ok_callback(self):
        images = [self.base_image_path_str]
        images.extend(self.controlnets_paths)
        self.app_settings.set_initial_images(images)
