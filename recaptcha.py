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
    'content-type': 'application/json'
}


def verify(token: str):
    payload = {
        "event": {
            "token": token,
            "siteKey": recaptcha_secret_key,
            "expectedAction": recaptcha_action_name
        }
    }
    return requests.post(verify_path, json=payload, headers=HEADERS).json()
