import json
import os

import numpy as np
import cv2

test_annotation_file = "./data/annotations/(10)A2766020.1.json"
test_image_file = "./data/images/(10)A2766020.1.png"
output_path = "./data/annotated_images/"

def get_annotations(annot_file):
    with open(annot_file, 'r') as f:
        annotations = json.loads(f.read())
    return annotations


def draw(image_file, annotation_file):
    image = cv2.imread(image_file)
    annotations = get_annotations(annotation_file)
    for annotation in annotations:
        vertices = np.array(annotation['bounding_box'])
        display_text = annotation['text']
        check_text = display_text.upper()
        if "DISPLAYSURFACE" in check_text or "SIGNBOARD" in check_text or "SIGNAGE" in check_text:
            cv2.polylines(image, [vertices], 1, (0, 0, 255), 3)
            cv2.putText(image, display_text,
                        tuple(vertices[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), thickness=2)
    cv2.imwrite(os.path.join(output_path, os.path.basename(image_file)), image)

if __name__ == "__main__":
    image_folder = "./data/images"
    annotation_folder = "./data/annotations"
    images = [os.path.join(image_folder, x) for x in os.listdir(image_folder)]
    annotations = [os.path.join(annotation_folder, x) for x in os.listdir(annotation_folder)]
    for i in range(len(images)):
        draw(images[i], annotations[i])