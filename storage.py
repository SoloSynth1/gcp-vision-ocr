import hashlib
import io

from google.cloud import storage
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "./key/credentials.json"


class GCPStorageAPI:

    def __init__(self):
        self.bucket_name = "bd-drawing-ocr-annotated-images"
        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        self.client = storage.Client(project=None, credentials=self.credentials)
        self.bucket = storage.bucket.Bucket(client=self.client, name=self.bucket_name)
        # self.hashlib =

    def list_bucket(self):
        response = self.client.list_blobs(self.bucket_name)
        return response

    def upload(self, buffer, content_type=None):
        blob_name = hashlib.sha1(buffer.getvalue()).hexdigest()
        print(blob_name)
        blob = storage.blob.Blob(name=blob_name, bucket=self.bucket)
        response = blob.upload_from_file(buffer, content_type=content_type, client=self.client)
        return response


if __name__ == "__main__":
    storage_api = GCPStorageAPI()
    test_file = "./data/annotated_images/(10)A2766020.1.png"
    with open(test_file, 'rb') as f:
        buffer = io.BytesIO(f.read())
    response = storage_api.upload(buffer, 'image/png')
    print(response)
