import requests

from environs import Env

env = Env()
env.read_env()
recaptcha_secret_key = env('RECAPTCHA_SECRET_KEY')
gcp_project_id = env('GCP_PROJECT_ID')
recaptcha_api_key = env('RECAPTCHA_API_KEY')
recaptcha_action_name = env('RECAPTCHA_ACTION_NAME')

verify_path = "https://recaptchaenterprise.googleapis.com/v1beta1/projects/{}/assessments?key={}".format(gcp_project_id, recaptcha_api_key)

HEADERS = {
    'content-type': 'application/json; charset=utf-8'
}


def verify(token: str, request_ip: str = None):
    # payload = {
    #     "secret": recaptcha_secret_key,
    #     "response": token,
    #     "remoteip": request_ip
    # }
    payload = {
        "event": {
            "token": token,
            "siteKey": recaptcha_secret_key,
            "expectedAction": "processImage"
        }
    }
    return requests.post(verify_path, data=payload, headers=HEADERS).json()

