from typing import Callable

from PIL.Image import Image


class BoundingBox:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def is_inside(self, x_pos, y_pos):
        return self.x_min <= x_pos <= self.x_max and self.y_min <= y_pos <= self.y_max

    def to_tuple(self) -> tuple[int, int, int, int]:
        return self.x_min, self.y_min, self.x_max, self.y_max

    def to_tuple_int(self) -> tuple[int, int, int, int]:
        return int(self.x_min), int(self.y_min), int(self.x_max), int(self.y_max)

    def resize(self, base_resolution: tuple[int, int], target_resolution: tuple[int, int]):
        x_min = self.x_min * target_resolution[0] / base_resolution[0]
        y_min = self.y_min * target_resolution[1] / base_resolution[1]
        x_max = self.x_max * target_resolution[0] / base_resolution[0]
        y_max = self.y_max * target_resolution[1] / base_resolution[1]
        return BoundingBox(int(x_min), int(y_min), int(x_max), int(y_max))

    def __repr__(self):
        return f"BoundingBox({self.x_min}, {self.y_min}, {self.x_max}, {self.y_max})"

    def print_width_height(self):
        print(f"Width: {self.x_max - self.x_min}, Height: {self.y_max - self.y_min}")


class SelectionBox:
    def __init__(self, id, x_size, y_size, x_pos, y_pos, outline='red'):
        self.id = id
        self.x_size = x_size
        self.y_size = y_size
        self.x_pos = x_pos  # center
        self.y_pos = y_pos  # center
        self.outline = outline
        self.initial_images: list[Image] = []
        self.replacement_image: Image = None
        self.on_replacement_image_changed: list[Callable[[SelectionBox], None]] = []

    def move_to(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def is_inside(self, x_pos, y_pos):
        return self.bounding_box().is_inside(x_pos, y_pos)

    def bounding_box(self) -> BoundingBox:
        x_min = self.x_pos - self.x_size / 2
        x_max = self.x_pos + self.x_size / 2
        y_min = self.y_pos - self.y_size / 2
        y_max = self.y_pos + self.y_size / 2
        return BoundingBox(x_min, y_min, x_max, y_max)

    def add_initial_image(self, image: Image):
        self.initial_images.append(image)

    def add_initial_images(self, images: list[Image]):
        self.initial_images.extend(images)

    def set_initial_images(self, images: list[Image]):
        self.initial_images = images

    def set_replacement_image(self, image: Image):
        self.replacement_image = image
        for callback in self.on_replacement_image_changed:
            callback(self)
