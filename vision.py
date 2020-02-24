from google.cloud import vision
from google.oauth2 import service_account


service_account_file = "./key/credentials.json"

credentials = service_account.Credentials.from_service_account_file(service_account_file)

client = vision.ImageAnnotatorClient(credentials=credentials)
response = client.annotate_image({
  'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
  'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
})
print(response)
