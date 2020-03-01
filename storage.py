import hashlib

from google.cloud import storage
from google.oauth2 import service_account


class GCPStorageAPI:

    def __init__(self, bucket_name, service_account_file):
        self.bucket_name = bucket_name
        self.public_uri = "https://storage.cloud.google.com/{}/".format(self.bucket_name)
        self.credentials = service_account.Credentials.from_service_account_file(service_account_file)
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