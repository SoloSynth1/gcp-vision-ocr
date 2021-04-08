from io import BytesIO
import base64

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from environs import Env

from vision import GCPVisionAPI
from storage import GCPStorageAPI
from signed_url import generate_signed_url
from visual import draw, write_to_buffer, read_from_btyes
from resize import get_resized_byte_string
from recaptcha import verify

env = Env()
env.read_env()

key_file = env('GCP_SERVICE_ACCOUNT_CREDENTIALS_PATH')
recaptcha_action_name = env('RECAPTCHA_ACTION_NAME')
gcp_bucket_name = env('GCP_BUCKET_NAME')
recaptcha_pass_threshold = env.float('RECAPTCHA_PASS_THRESHOLD')

app = Flask(__name__)
CORS(app)

vision_api = GCPVisionAPI(key_file)
storage_api = GCPStorageAPI(gcp_bucket_name, key_file)


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
    signed_url = generate_signed_url(service_account_file=key_file,
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
        assessment = verify(recaptcha_token, ip_address)
        print("assessment results: {}".format(assessment))
        properties = assessment.get('tokenProperties')
        if properties and properties.get('valid') is True and properties.get("action") == recaptcha_action_name and \
                assessment.get('score') >= recaptcha_pass_threshold:
                response = jsonify(process_request(content))
                return response
    response = jsonify({"error": "recaptcha assessment failed"})
    response.status_code = 403
    return response


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
