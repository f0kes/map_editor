from PIL import Image

from box import SelectionBox


def paste_replacement(image: Image.Image, box: SelectionBox):
    replacement = box.replacement_image
    if replacement is not None:
        print(box.bounding_box().to_tuple())

        image.paste(replacement, box.bounding_box().to_tuple_int())


def paste_original(image: Image.Image, box: SelectionBox):
    original = box.initial_images[0]
    if original is not None:
        image.paste(original, box.bounding_box().to_tuple_int())
