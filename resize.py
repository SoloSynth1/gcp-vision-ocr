import os

from PIL import Image

raw_files = "./raw"
output_path = "./data/images"

def resize(image_file, dst):
    image = Image.open(image_file)
    width, height = image.size
    resized_image = image.resize((width//2, height//2))
    resized_image.save(os.path.join(dst, os.path.basename(image_file).replace(".tif", ".png")))

if __name__ == "__main__":
    images = [os.path.join(raw_files, x) for x in os.listdir(raw_files) if ".tif" in x]
    for image in images:
        resize(image, output_path)