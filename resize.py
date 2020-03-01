import os
from io import BytesIO

from PIL import Image

raw_files = "./raw"
output_path = "./data/images"


def bytes_to_image(byte_string):
    buffer = BytesIO(byte_string)
    image = Image.open(buffer)
    return image


def get_resized_byte_string(image, total_byte_limit=900000):
    # set to 900000 since vision api only accept json request no larger than 1024 * 1024 = 1,048,576 bytes
    while True:
        with BytesIO() as output:
            image.save(output, format="png")
            byte_string = output.getvalue()
        if len(byte_string) > total_byte_limit:
            width, height = image.size
            image = image.resize((width//2, height//2))
        else:
            print(image.size)
            break
    return byte_string

#
# def save(image, dst):
#     image.save(os.path.join(dst, os.path.basename(image_file).replace(".tif", ".png")))
