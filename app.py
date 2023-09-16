import yaml
from flask import Flask, request

import livetex_client

app = Flask(__name__)

BASE_URL = '/bot-api/webhook'
CONVERSATION_TREE_FILE = 'conversation_tree.yml'


@app.route(BASE_URL, methods=['POST'])
def get_reply() -> list:
    data = request.json
    response = []
    if data.get('type') in ('VisitorButtonPressed', 'VisitorTextSent'):
        channel_id = data.get('channelId')
        visitor_id = data.get('visitorId')
        path = data.get('payload', 'root').split('.')
        response.append(livetex_client.send_reply(channel_id, visitor_id, build_payload(path)))
        if path[-1] == 'operator':
            response.append(livetex_client.transfer_to_operator(channel_id, visitor_id))
    return response


@app.route(BASE_URL, methods=['GET'])
def get_settings() -> dict:
    return build_payload(['root'])


def get_node(path):
    node = get_conversation_tree(CONVERSATION_TREE_FILE)
    for key in path:
        node = node.get('children', node).get(key, {})
    return node


def build_payload(path):
    node = get_node(path)
    buttons = []
    children = node.get('children')
    if children:
        for key, value in children.items():
            buttons.append({
                'type': 'textButton',
                'label': value.get('button'),
                'payload': '.'.join(path + [key])
            })
    if path[-1] not in ('root', 'operator'):
        buttons.append({
            'type': 'textButton',
            'label': 'Назад',
            'payload': 'root'
        })
    return {
        'text': node.get('text'),
        'buttons': buttons,
        'path': path
    }


def get_conversation_tree(file):
    with open(file, 'r') as replies_file:
        return yaml.safe_load(replies_file)


if __name__ == '__main__':
    app.run()
