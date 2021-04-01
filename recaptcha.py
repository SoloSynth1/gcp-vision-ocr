import requests

from environs import Env

env = Env()
env.read_env()
recaptcha_secret_key = env('RECAPTCHA_SECRET_KEY')

verify_path = "https://www.google.com/recaptcha/api/siteverify"


def verify(token: str, request_ip: str = None):
    payload = {
        "secret": recaptcha_secret_key,
        "response": token,
        "remoteip": request_ip
    }
    return requests.post(verify_path, data=payload).json()

