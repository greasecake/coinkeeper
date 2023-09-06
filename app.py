import yaml
from flask import Flask, request

import livetex_client

app = Flask(__name__)

BASE_URL = '/bot-api/webhook'

if __name__ == '__main__':
    app.run()


@app.route(BASE_URL, methods=['POST'])
def get_reply():
    data = request.json
    channel_id = data.get('channelId')
    visitor_id = data.get('visitorId')
    keys = data.get('payload', 'root').split('.')
    response = []
    if data.get('type') in (
            'VisitorButtonPressed',
            'VisitorTextSent',
            'VisitorFileSent',
    ):
        response.append(livetex_client.send_reply(channel_id, visitor_id, build_payload(keys)))
        if keys[-1] == 'operator':
            response.append(livetex_client.connect_to_operator(channel_id, visitor_id))
    return response


@app.route(BASE_URL, methods=['GET'])
def get_settings():
    return build_payload({'payload': 'root'})


def get_reply_tree():
    with open('script.yml', 'r') as replies_file:
        return yaml.safe_load(replies_file)


def get_node(keys: list):
    node: dict = get_reply_tree()
    for key in keys:
        node = node.get('children', node).get(key, {})
    return node


def build_payload(keys):
    node = get_node(keys)
    buttons = []
    children = node.get('children')
    if children:
        for key, value in children.items():
            buttons.append({
                'type': 'textButton',
                'label': value.get('button'),
                'payload': '.'.join(keys + [key])
            })
    if keys[-1] not in ('root', 'operator'):
        buttons.append({
            'type': 'textButton',
            'label': 'Назад',
            'payload': 'root'
        })
    return {
        'text': node.get('text'),
        'buttons': buttons,
        'path': keys
    }
