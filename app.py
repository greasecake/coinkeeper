import yaml
from flask import Flask, request, jsonify

from livetex_client import send_text, route_to_operator

app = Flask(__name__)

BASE_URL = '/bot-api/webhook'


@app.route(BASE_URL, methods=['POST'])
def get_reply():
    data = request.json
    channel_id = data.get('channelId')
    visitor_id = data.get('visitorId')
    code, payload = __build_payload(data)
    if data.get('type') in ('VisitorButtonPressed', 'VisitorTextSent'):
        send_text(channel_id, visitor_id, payload)
        if code == 'operator':
            route_to_operator(channel_id, visitor_id)
    return {
        'status': 'success',
        'visitor_id': visitor_id,
        'channel_id': channel_id
    }


@app.route(BASE_URL, methods=['GET'])
def get_settings():
    return __build_payload({'payload': 'root'})[1]


def __get_reply_tree():
    with open('script.yml', 'r') as replies_file:
        return yaml.safe_load(replies_file)


def __get_node(keys: list):
    node: dict = __get_reply_tree()
    for key in keys:
        node = node.get('children', node).get(key, {})
    return node


def __build_payload(data):
    path = data.get('payload', 'root')
    keys = path.split('.')
    node = __get_node(keys)
    buttons = []
    children = node.get('children')
    if children:
        for key, value in children.items():
            buttons.append({
                'type': 'textButton',
                'label': value.get('button'),
                'payload': f'{path}.{key}'
            })
        if keys[-1] != 'root':
            buttons.append({
                'type': 'textButton',
                'label': 'Назад',
                'payload': 'root'
            })
    return keys[-1], {
        'text': node.get('text'),
        'buttons': buttons
    }


if __name__ == '__main__':
    app.run()
