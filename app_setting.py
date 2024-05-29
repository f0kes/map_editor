import os
import subprocess
import sys
from typing import Callable

import image_cutter
from box import SelectionBox
from PIL.Image import Image
from box_replacer import paste_replacement, paste_original
import PIL


class AppSettings:
    def __init__(self, image: Image, image_cutter: image_cutter.ImageCutter, selected_color='green',
                 unselected_color='red'):
        self.base_image = image
        self.initial_images = [image]
        self.select_x_size = 0
        self.select_y_size = 0
        self.selected_color = selected_color
        self.unselected_color = unselected_color
        self.boxes = []
        self.selected_box = None
        self.image_cutter = image_cutter
        self.on_box_selected = []
        self.on_image_chaged = []
        self.current_box_id = 0

    def set_x_size(self, x_size):
        print("x_size: ", x_size)
        self.select_x_size = x_size

    def set_y_size(self, y_size):
        print("y_size: ", y_size)
        self.select_y_size = y_size

    def add_box(self, box: SelectionBox):
        self.boxes.append(box)

    def get_box_at_pos(self, x_pos, y_pos):
        for box in self.boxes:
            if box.is_inside(x_pos, y_pos):
                return box
        return None

    def select_box(self, box: SelectionBox):
        if self.selected_box is not None:
            self.selected_box.outline = self.unselected_color
        self.selected_box = box
        self.selected_box.outline = self.selected_color
        for callback in self.on_box_selected:
            callback(box)

    def create_box(self, x_pos, y_pos):
        box = SelectionBox(self.current_box_id, self.select_x_size, self.select_y_size, x_pos, y_pos)
        self.current_box_id += 1
        self.add_box(box)
        images = self.image_cutter.crop_all(box)
        box.add_initial_images(images)
        box.on_replacement_image_changed += [self.on_replace_image]
        self.select_box(box)

    def get_or_create_box(self, x_pos, y_pos):
        box = self.get_box_at_pos(x_pos, y_pos)
        if box is None:
            self.create_box(x_pos, y_pos)
        else:
            self.select_box(box)

    def delete_box_at_pos(self, x_pos, y_pos):
        box = self.get_box_at_pos(x_pos, y_pos)
        if box is not None:
            self.boxes.remove(box)
            self.selected_box = None

    def add_box_selected_callback(self, callback: Callable[[SelectionBox], None]):
        self.on_box_selected += [callback]

    def add_image_changed_callback(self, callback: Callable[[Image], None]):
        self.on_image_chaged += [callback]

    def on_replace_image(self, box: SelectionBox):
        paste_replacement(self.base_image, box)
        for callback in self.on_image_chaged:
            callback(self.base_image)

    def delete_current_box(self):
        if self.selected_box is not None:
            self.boxes.remove(self.selected_box)
            paste_original(self.base_image, self.selected_box)
            for callback in self.on_image_chaged:
                callback(self.base_image)
            self.selected_box = None

    def export_original(self):
        # save current box initaial images to folder
        inital_images = self.selected_box.initial_images
        path = f"./box_{self.selected_box.id}"
        if not os.path.exists(path):
            os.makedirs(path)
        for i, image in enumerate(inital_images):
            # then save image to that folder
            image.save(f"{path}/image_{i}.png")
        open_file(path)

    def set_initial_images(self, images):
        self.base_image = PIL.Image.open(images[0])
        new_images = [self.base_image]
        new_images.extend([PIL.Image.open(image) for image in images[1:]])
        self.initial_images = new_images
        self.boxes = []
        self.image_cutter.update_images(new_images)
        for callback in self.on_image_chaged:
            callback(self.base_image)

    def save_image(self):
        path = "./output.png"
        self.base_image.save(path)
        open_file(path)


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
