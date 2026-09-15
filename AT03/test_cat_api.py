from unittest.mock import Mock, patch

from cat_api import get_random_cat_image


@patch("cat_api.requests.get")
def test_successful_request_returns_url(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"url": "https://cdn.thecatapi.com/images/abc.jpg"}]
    mock_get.return_value = mock_response

    assert get_random_cat_image() == "https://cdn.thecatapi.com/images/abc.jpg"


@patch("cat_api.requests.get")
def test_not_found_returns_none(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    assert get_random_cat_image() is None
