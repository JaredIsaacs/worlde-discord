from globals import *
import requests

def get_wordle_info(word: str):
    body = {
    "guess": word
    }

    return requests.post(url=WORDLE_URL, data=body).json()
