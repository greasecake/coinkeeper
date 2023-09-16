import livetex_client


def test_send_reply_success(mock_channel_token_mapping, mock_livetex_success_response):
    result = livetex_client.send_reply('channel_id', 'visitor_id', {})
    assert result.get('response_result') == 'success'


def test_send_reply_error_200(mock_channel_token_mapping, mock_livetex_error_response_200):
    result = livetex_client.send_reply('channel_id', 'visitor_id', {})
    assert result.get('response_result') == 'error'


def test_send_reply_error_403(mock_channel_token_mapping, mock_livetex_error_response_403):
    result = livetex_client.send_reply('channel_id', 'visitor_id', {})
    assert result.get('response_result') == 'error'


def test_send_reply_error_500(mock_channel_token_mapping, mock_livetex_error_response_500):
    result = livetex_client.send_reply('channel_id', 'visitor_id', {})
    assert result.get('response_result') == 'error'
