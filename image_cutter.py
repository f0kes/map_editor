from PIL import Image
from box import SelectionBox


class ImageCutter:
    def __init__(self, images: list[Image.Image]):
        self.base_image = images[0]
        self.reference_images = images[1:]
        self.base_resolution = self.base_image.size

    def crop_with_box(self, image: Image.Image, box: SelectionBox) -> Image.Image:
        target_resolution = image.size
        bounding_box = (box
                        .bounding_box()
                        .resize(self.base_resolution, target_resolution)
                        .to_tuple_int())
        return image.crop(bounding_box)

    def crop_all(self, box: SelectionBox) -> list[Image.Image]:
        references = [self.crop_with_box(image, box) for image in self.reference_images]
        base = self.crop_with_box(self.base_image, box)
        all_cropped = [base] + references
        return all_cropped

    def update_images(self, images: list[Image.Image]):
        self.base_image = images[0]
        self.reference_images = images[1:]
        self.base_resolution = self.base_image.size
