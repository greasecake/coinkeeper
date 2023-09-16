import logging
from unittest.mock import Mock, patch

import pytest

import app


@pytest.fixture(autouse=True)
def disable_logging(caplog):
    caplog.set_level(logging.CRITICAL)


@pytest.fixture
def mock_channel_token_mapping():
    with patch(
        'livetex_client.get_channel_token_mapping',
        return_value={'channel_id': 'token'}
    ):
        yield


@pytest.fixture
def mock_livetex_success_response():
    with patch(
        'requests.Session.request',
        return_value=Mock(status_code=200, json=lambda: {})
    ):
        yield


@pytest.fixture
def mock_livetex_error_response_200():
    with patch(
        'requests.Session.request',
        return_value=Mock(status_code=200, json=lambda: {'error': 'trace'})
    ):
        yield


@pytest.fixture
def mock_livetex_error_response_403():
    with patch(
        'requests.Session.request',
        return_value=Mock(status_code=401, json=lambda: {})
    ):
        yield


@pytest.fixture
def mock_livetex_error_response_500():
    with patch(
        'requests.Session.request',
        return_value=Mock(status_code=500, json=lambda: {})
    ):
        yield


@pytest.fixture
def mock_livetex_send_reply_success():
    with patch(
        'livetex_client.send_reply',
        return_value={'status': 'success'}
    ):
        yield


@pytest.fixture
def mock_livetex_transfer_to_operator_success():
    with patch(
        'livetex_client.transfer_to_operator',
        return_value={'status': 'success'}
    ):
        yield


@pytest.fixture
def mock_app():
    with app.app.test_client() as client:
        yield client


@pytest.fixture
def mock_conversation_tree_valid():
    with patch(
        'app.get_conversation_tree',
        return_value={
            'root': {
                'text': 'root_text',
                'children': {
                    'option': {
                        'button': 'option_button',
                        'text': 'option_text'
                    },
                    'operator': {
                        'button': 'operator_button',
                        'text': 'operator_text'
                    }
                }
            }
        }
    ):
        yield
