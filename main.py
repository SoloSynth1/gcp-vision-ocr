import os

from bytify import get_byte_string_from_image
from vision import GCPVisionAPI
from visual import draw, write_to_buffer, read_from_btyes
from storage import GCPStorageAPI
from signed_url import generate_signed_url

output_path = "./data/annotations"


def annotate_and_upload(image_byte_string, expiration=600):
    response = vision_api.get_text_annotations(image_byte_string)
    paragraphs = vision_api.parse_response_to_paragraphs(response)
    image = read_from_btyes(image_byte_string)
    annotated_image = draw(image, paragraphs)
    buffer = write_to_buffer(annotated_image)
    storage_api = GCPStorageAPI()
    blob_name, uploaded_link = storage_api.upload(buffer, 'image/png')
    signed_url = generate_signed_url(service_account_file="./key/credentials.json", bucket_name=storage_api.bucket_name,
                                     object_name=blob_name, subresource=None, expiration=expiration, http_method='GET',
                                     query_parameters=None, headers=None)
    return signed_url


if __name__ == "__main__":

    vision_api = GCPVisionAPI()
    storage_api = GCPStorageAPI()

    image_folder = "./data/images"
    images = [os.path.join(image_folder, x) for x in os.listdir(image_folder)]

    for image in images:
        byte_string = get_byte_string_from_image(image)
        signed_url = annotate_and_upload(byte_string, expiration=3600)
        print(signed_url)



