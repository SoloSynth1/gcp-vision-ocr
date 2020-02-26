import json

import numpy as np
import cv2

test_annotation_file = "./data/annotations/(2)A2766008.1.json"
test_image_file = "./data/images/(2)A2766008.1.png"


def get_annotations(annot_file):
    with open(annot_file, 'r') as f:
        annotations = json.loads(f.read())
    return annotations


def draw():
    image = cv2.imread(test_image_file)
    annotations = get_annotations(test_annotation_file)
    for annotation in annotations:
        vertices = np.array(annotation['bounding_box'])
        display_text = annotation['text']
        check_text = display_text.upper()
        if "DISPLAYSURFACE" in check_text or "SIGNBOARD" in check_text or "SIGNAGE" in check_text:
            cv2.polylines(image, [vertices], 1, (0, 255, 0), 3)
            cv2.putText(image, display_text,
                        tuple(vertices[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)
    winname = "test"
    cv2.imshow(winname, image)
    cv2.waitKey()
    cv2.destroyWindow(winname)

if __name__ == "__main__":
    draw()