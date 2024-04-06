from pygame.image import load
from pygame.transform import scale
from PIL import Image


def resize_image(image_path, desired_width) -> Image:
    image = load(image_path)
    # Calculate aspect ratio
    aspect_ratio = image.get_height() / image.get_width()

    # Calculate the corresponding new height
    new_height = round(desired_width * aspect_ratio)

    resized_image = scale(image, (desired_width, new_height))
    return resized_image
