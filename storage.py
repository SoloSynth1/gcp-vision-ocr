import hashlib
import io

from google.cloud import storage
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "./key/credentials.json"


class GCPStorageAPI:

    def __init__(self):
        self.bucket_name = "bd-drawing-ocr-annotated-images"
        self.public_uri = "https://storage.cloud.google.com/{}/".format(self.bucket_name)
        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        self.client = storage.Client(project=None, credentials=self.credentials)
        self.bucket = storage.bucket.Bucket(client=self.client, name=self.bucket_name)
        # self.hashlib =

    def list_bucket(self):
        response = self.client.list_blobs(self.bucket_name)
        return response

    def upload(self, buffer, content_type=None):
        blob_name = hashlib.sha1(buffer.getvalue()).hexdigest()
        blob = storage.blob.Blob(name=blob_name, bucket=self.bucket)
        blob.upload_from_file(buffer, content_type=content_type, client=self.client)
        return blob_name, self.public_uri + blob_name


if __name__ == "__main__":
    storage_api = GCPStorageAPI()
    test_file = "./data/annotated_images/(3)A2800406.1.png"
    with open(test_file, 'rb') as f:
        buffer = io.BytesIO(f.read())
    uploaded_link = storage_api.upload(buffer, 'image/png')
    print(uploaded_link)
