import os
from io import BytesIO

from PIL import Image

raw_files = "./raw"
output_path = "./data/images"


def bytes_to_image(byte_string):
    buffer = BytesIO(byte_string)
    image = Image.open(buffer)
    return image


def resize(image, total_pixel_limit=40000000):
    width, height = image.size
    while (width*height > total_pixel_limit):
        image = image.resize((width//2, height//2))
        width, height = image.size
    return image


def save(image, dst):
    image.save(os.path.join(dst, os.path.basename(image_file).replace(".tif", ".png")))


if __name__ == "__main__":
    image_files = [os.path.join(raw_files, x) for x in os.listdir(raw_files) if ".tif" in x]
    for image_file in image_files:
        image = Image.open(image_file)
        resized_image = resize(image)
        save(resized_image, output_path)