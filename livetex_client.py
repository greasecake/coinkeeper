import json
import logging

import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry

LIVETEX_URL = 'https://bot-api.livetex.ru'
CHANNEL_TOKEN_MAPPING_FILE = 'channel_tokens.json'

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
    response = make_request(
        channel_id,
        f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/text',
        payload,
    )
    return handle_response(channel_id, visitor_id, 'send_reply', response, payload=payload.get('path'))


def transfer_to_operator(channel_id, visitor_id):
    response = make_request(channel_id, f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/route', {})
    return handle_response(channel_id, visitor_id, 'transfer_to_operator', response)


def make_request(channel_id, url, payload, method='POST'):
    try:
        response = session.request(
            method,
            url,
            json=payload,
            headers=build_headers(channel_id)
        )
        return response
    except requests.exceptions.RequestException as e:
        return None


def handle_response(channel_id, visitor_id, request_type, response, **kwargs):
    response_result = get_response_result(response)
    result = {
        'channel_id': channel_id,
        'visitor_id': visitor_id,
        'request_type': request_type,
        'response_result': response_result,
        'response_code': response.status_code,
        **kwargs
    }
    logger.log(
        msg=result,
        level=(logging.ERROR if response_result == 'error' else logging.DEBUG)
    )
    return result


def get_response_result(response: Response):
    if (
            response is None or
            str(response.status_code).startswith('4') or
            response.status_code == 200 and response.content and response.json().get('error')
    ):
        return 'error'
    if response.status_code == 200:
        return 'success'
    return 'error'


def get_channel_token_mapping(file):
    with open(file, 'r') as config_file:
        return json.load(config_file)


def build_headers(channel_id):
    return {
        'Content-Type': 'application/json',
        'Bot-Api-Token': get_channel_token_mapping(CHANNEL_TOKEN_MAPPING_FILE).get(str(channel_id))
    }
