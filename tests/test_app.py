import yaml
from jsonschema import validate

import app


def test_validate_conversation_tree():
    with open('schema.yml', 'r') as schema_file:
        validate(
            app.get_conversation_tree(f'{app.app.root_path}/{app.CONVERSATION_TREE_FILE}'),
            yaml.safe_load(schema_file)
        )


def test_get_reply(
        mock_app,
        mock_conversation_tree_valid,
        mock_livetex_send_reply_success,
        mock_livetex_transfer_to_operator_success
):
    response = mock_app.post(app.BASE_URL, json={
        'type': 'VisitorTextSent',
        'channelId': 'channelId',
        'visitorId': 'visitorId',
        'payload': 'root.option1',
    }).json
    assert isinstance(response, list)
    assert len(response) == 1


def test_build_payload_root(mock_conversation_tree_valid):
    payload = app.build_payload(['root'])
    assert payload.get('text') == 'root_text'
    assert len(payload.get('buttons')) == 2
    assert payload.get('path') == ['root']


def test_build_payload_option(mock_conversation_tree_valid):
    payload = app.build_payload(['root', 'option'])
    assert payload.get('text') == 'option_text'
    assert len(payload.get('buttons')) == 1
    assert payload.get('path') == ['root', 'option']


def test_build_payload_operator(mock_conversation_tree_valid):
    payload = app.build_payload(['root', 'operator'])
    assert payload.get('text') == 'operator_text'
    assert len(payload.get('buttons')) == 0
    assert payload.get('path') == ['root', 'operator']
