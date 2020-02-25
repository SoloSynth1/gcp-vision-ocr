from google.cloud import vision
from google.oauth2 import service_account

from bytify import get_sample_byte_string


SERVICE_ACCOUNT_FILE = "./key/credentials.json"


class GCPVisionAPI:

    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)


    def get_text_annotations(self, image_btye_string):
        response = self.client.text_detection({'content': image_btye_string})
        return response

    def parse_response_to_paragraphs(self, response):
        paragraphs = []
        first_page_annotations = response.full_text_annotation.pages[0]
        for block in first_page_annotations.blocks:
            for paragraph in block.paragraphs:
                paragraph_texts = []
                for word in paragraph.words:
                    for symbol in word.symbols:
                        paragraph_texts.append(symbol.text)
                paragraph_text = ''.join(paragraph_texts)
                bounding_box = []
                for vertice in paragraph.bounding_box.vertices:
                    bounding_box.append((vertice.x, vertice.y))
                paragraphs.append({"text": paragraph_text,
                                   "bounding_box": bounding_box})
        return paragraphs


if __name__ == "__main__":
    vision_api = GCPVisionAPI()
    response = vision_api.get_text_annotations(get_sample_byte_string())
    paragraphs = vision_api.parse_response_to_paragraphs(response)
    print(paragraphs)


