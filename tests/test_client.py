# tests/test_expedia_client.py
import pytest
import requests
from unittest.mock import patch, MagicMock
from expedia_travel_recommendations.api.client import ExpediaApiClient


@pytest.fixture
def client(monkeypatch):
    # Set a fake API key in env
    monkeypatch.setenv("EXPEDIA_API_KEY", "fake_api_key")
    return ExpediaApiClient()


@pytest.mark.parametrize(
    "method_name,endpoint",
    [
        ("get_hotel_recommendations", "/recommendations/hotels"),
        ("get_flight_recommendations", "/recommendations/flights"),
        ("get_activity_recommendations", "/recommendations/activities"),
        ("get_car_recommendations", "/recommendations/cars"),
    ],
)
def test_api_methods_call_requests(client, method_name, endpoint):
    """Test that each API method calls requests.get with the right URL and headers."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"result": "ok"}

    with patch(
        "expedia_travel_recommendations.api.client.requests.get",
        return_value=fake_response,
    ) as mock_get:
        method = getattr(client, method_name)
        response = method(param1="value1", param2="value2")

        assert response == {"result": "ok"}
        mock_get.assert_called()

        # URL is the first positional argument
        called_url = mock_get.call_args[0][0]
        assert called_url == client.base_url + endpoint

        # headers are keyword arguments
        headers = mock_get.call_args[1]["headers"]
        assert headers["X-API-KEY"] == "fake_api_key"


def test_make_request_unauthorized_fallback(client):
    """Test that 401 triggers fallback to basic auth."""
    # First response 401, second response 200
    response_401 = MagicMock()
    response_401.status_code = 401
    response_401.raise_for_status.side_effect = None
    response_401.json.return_value = {"error": "unauthorized"}

    response_200 = MagicMock()
    response_200.status_code = 200
    response_200.json.return_value = {"result": "ok"}

    with patch(
        "expedia_travel_recommendations.api.client.requests.get",
        side_effect=[response_401, response_200],
    ) as mock_get:
        result = client._make_request(
            "/recommendations/hotels",
            {"user_input_in_english": "Paris", "keywords": "Hotels"},
        )
        assert result == {"result": "ok"}
        assert mock_get.call_count == 2


def test_make_request_exception(client):
    """Test that exceptions are caught and returned as error dict."""
    with patch("expedia_travel_recommendations.api.client.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        result = client._make_request(
            "/recommendations/hotels",
            {"user_input_in_english": "Paris", "keywords": "Hotels"},
        )
        assert "error" in result
        assert "Connection error" in result["error"]
        assert "url" in result
        assert "params" in result
