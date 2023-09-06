import logging
import os

import requests
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv

load_dotenv()
LIVETEX_URL = 'https://bot-api.livetex.ru'
headers = {
    'Content-Type': 'application/json',
    'Bot-Api-Token': os.environ.get('LIVETEX_TOKEN')
}

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
logger.addHandler(file_handler)


def send_reply(channel_id, visitor_id, payload):
    try:
        session.post(
            f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/text',
            json=payload,
            headers=headers
        )
        response = build_response(channel_id, visitor_id, 'success', payload=payload.get('path'))
        logger.debug(response)
    except requests.exceptions.RequestException as exception:
        response = build_response(channel_id, visitor_id, 'error', payload=payload.get('path'), result=exception)
        logger.error(response)
    return response


def connect_to_operator(channel_id, visitor_id):
    try:
        session.post(
            f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/route',
            json={},
            headers=headers
        )
        response = build_response(channel_id, visitor_id, 'success')
        logger.debug(response)
    except requests.exceptions.RequestException as exception:
        response = build_response(channel_id, visitor_id, 'error', result=exception)
        logger.error(response)
    return response


def build_response(channel_id, visitor_id, status, **kwargs):
    return {
        'channel_id': channel_id,
        'visitor_id': visitor_id,
        'status': status,
        **kwargs
    }
