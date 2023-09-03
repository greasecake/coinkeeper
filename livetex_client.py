import os

import requests
from dotenv import load_dotenv

load_dotenv()
LIVETEX_URL = 'https://bot-api.livetex.ru'

headers = {
    'Content-Type': 'application/json',
    'Bot-Api-Token': os.environ.get('LIVETEX_TOKEN')
}


def send_text(channel_id, visitor_id, payload):
    requests.post(
        f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/text',
        json=payload,
        headers=headers
    )


def route_to_operator(channel_id, visitor_id):
    requests.post(
        f'{LIVETEX_URL}/v1/channel/{channel_id}/visitor/{visitor_id}/route',
        json={},
        headers=headers
    )
