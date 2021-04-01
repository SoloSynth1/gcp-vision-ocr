from io import BytesIO
import base64

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

from vision import GCPVisionAPI
from storage import GCPStorageAPI
from signed_url import generate_signed_url
from visual import draw, write_to_buffer, read_from_btyes
from resize import get_resized_byte_string
from recaptcha import verify

app = Flask(__name__)
CORS(app)

BUCKET_NAME = "deadly-python"
KEY_FILE = "./key/credentials.json"
RECAPTCHA_PASS_THRESHOLD = 0.7

vision_api = GCPVisionAPI(KEY_FILE)
storage_api = GCPStorageAPI(BUCKET_NAME, KEY_FILE)


def annotate_and_upload(image_byte_string, criteria, vision_api, storage_api):
    response = vision_api.get_text_annotations(image_byte_string)
    paragraphs = vision_api.parse_response_to_paragraphs(response)
    image = read_from_btyes(image_byte_string)
    annotated_image = draw(image, paragraphs, criteria)
    buffer = write_to_buffer(annotated_image)
    blob_name, uploaded_link = storage_api.upload(buffer, 'image/png')
    return blob_name, uploaded_link


def process_request(content):
    base64_encoded_image = content['image']
    criteria = content['criteria']
    byte_string = base64.b64decode(base64_encoded_image)
    buffer = BytesIO(byte_string)
    image = Image.open(buffer)
    resized_byte_string = get_resized_byte_string(image)

    blob_name, uploaded_link = annotate_and_upload(resized_byte_string, criteria, vision_api, storage_api)
    signed_url = generate_signed_url(service_account_file=KEY_FILE,
                                     bucket_name=storage_api.bucket_name,
                                     object_name=blob_name, subresource=None, expiration=3600,
                                     http_method='GET',
                                     query_parameters=None, headers=None)
    return {"annotatedImage": signed_url}


@app.route('/process', methods=['POST'])
def process_image():
    content = request.get_json()
    ip_address = request.remote_addr
    recaptcha_token = content.get("token")
    if recaptcha_token:
        recaptcha_assessment = verify(recaptcha_token, ip_address)
        print("assessment results: {}".format(recaptcha_assessment))
        if recaptcha_assessment.get('success') and recaptcha_assessment.get('score') >= RECAPTCHA_PASS_THRESHOLD:
            response = jsonify(process_request(content))
            return response
        else:
            response = jsonify({"error": "recaptcha assessment failed"})
            response.status_code = 403
            return response
    else:
        response = jsonify({"error": "recaptcha assessment failed"})
        response.status_code = 403
        return response


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
