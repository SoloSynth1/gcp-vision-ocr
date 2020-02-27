from io import BytesIO
import base64

from flask import Flask, request, jsonify
from PIL import Image

from vision import GCPVisionAPI
from storage import GCPStorageAPI
from signed_url import generate_signed_url
from main import annotate_and_upload
from resize import get_resized_byte_string

app = Flask(__name__)

vision_api = GCPVisionAPI()
storage_api = GCPStorageAPI()


@app.route('/process', methods=['POST'])
def process_image():
    content = request.get_json()
    base64_encoded_image = content['image']
    criteria = content['criteria']
    byte_string = base64.b64decode(base64_encoded_image)
    buffer = BytesIO(byte_string)
    image = Image.open(buffer)
    resized_byte_string = get_resized_byte_string(image)

    blob_name, uploaded_link = annotate_and_upload(resized_byte_string, criteria, vision_api, storage_api)
    signed_url = generate_signed_url(service_account_file="./key/credentials.json",
                                     bucket_name=storage_api.bucket_name,
                                     object_name=blob_name, subresource=None, expiration=3600,
                                     http_method='GET',
                                     query_parameters=None, headers=None)
    response = {"signed_url": signed_url}
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
