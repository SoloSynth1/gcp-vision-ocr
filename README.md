# gcp-vision-ocr

Containerized flask app to perform OCR and highlight words on images.

Stores image on Google Cloud Storage and return a signed URL with expiration time.

Now supports reCAPTCHA Enterprise!

## Installation

1. Enable Cloud Storage API & Vision API on your GCP project.

2. Create a service account and put the credentials (in JSON format) in `key/credentials.json`.

3. Use the docker to build image.

```bash
docker build . --tag={tag-name-goes-here}
```

Then run on your favorite platform.
```bash
docker run -p8080:8080 {tag-name-goes-here}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
