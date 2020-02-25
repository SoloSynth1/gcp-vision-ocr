import os
import json

from bytify import get_byte_string_from_image
from vision import GCPVisionAPI

output_path = "./data/annotations"

if __name__ == "__main__":

    vision_api = GCPVisionAPI()

    image_folder = "./data/images"
    images = [os.path.join(image_folder, x) for x in os.listdir(image_folder)]

    for image in images:
        byte_string = get_byte_string_from_image(image)
        response = vision_api.get_text_annotations(byte_string)
        paragraphs = vision_api.parse_response_to_paragraphs(response)
        with open(os.path.join(output_path, os.path.basename(image).replace(".png", ".json")), "w") as f:
            f.write(json.dumps(paragraphs))

