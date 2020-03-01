import json
import io

import numpy as np
import cv2

test_annotation_file = "./data/annotations/(10)A2766020.1.json"
test_image_file = "./data/images/(10)A2766020.1.png"
output_path = "./data/annotated_images/"


def get_annotations(annot_file):
    with open(annot_file, 'r') as f:
        annotations = json.loads(f.read())
    return annotations


def read_from_btyes(byte_string):
    nparr = np.fromstring(byte_string, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image


def contains_text(text, criteria):
    for criterion in criteria:
        if criterion.upper().replace(" ", "") in text.upper():
            return True
    return False


def draw(image, annotations, criteria):
    for annotation in annotations:
        vertices = np.array(annotation['bounding_box'])
        display_text = annotation['text']
        check_text = display_text.upper()
        if contains_text(check_text, criteria):
            cv2.polylines(image, [vertices], 1, (0, 0, 255), 3)
            cv2.putText(image, display_text,
                        tuple(vertices[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), thickness=2)
    return image


def write_to_file(image, target):
    cv2.imwrite(target, image)


def write_to_buffer(image):
    is_success, cv_buffer = cv2.imencode(".png", image)
    buffer = io.BytesIO(cv_buffer)
    return buffer
