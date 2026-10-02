# tests/test_handlers.py
import asyncio
import threading
import pytest
from unittest.mock import patch
from expedia_travel_recommendations.api import handlers


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["hotel", "flight", "activity", "car"])
async def test_api_request_does_not_block_event_loop(mock_client, kind):
    release = threading.Event()
    client_method = getattr(mock_client, f"get_{kind}_recommendations")
    client_method.side_effect = lambda **kwargs: {"responsive": release.wait(timeout=2)}
    params = {
        "destination": "Paris",
        "origin": "London",
        "pickup_location": "Paris",
        "user_input_in_english": "Travel to Paris",
        "keywords": "Travel",
    }
    handler = getattr(handlers, f"process_{kind}_query")
    task = asyncio.create_task(handler(params))
    # This callback can only release the request if the handler yields to the loop.
    asyncio.get_running_loop().call_soon(release.set)
    try:
        assert await task == {"responsive": True}
    finally:
        release.set()
    client_method.assert_called_once_with(**params)


@pytest.fixture
def mock_client():
    """Patch the ExpediaApiClient in handlers to avoid real API calls."""
    with patch("expedia_travel_recommendations.api.handlers.api_client") as mock:
        yield mock


@pytest.mark.asyncio
async def test_process_hotel_query_required_params(mock_client):
    # Missing destination
    result = await handlers.process_hotel_query(
        {"user_input_in_english": "Hotels in Paris", "keywords": "Hotels"}
    )
    assert "error" in result and "Destination is required" in result["error"]

    # Missing user_input_in_english
    result = await handlers.process_hotel_query(
        {"destination": "Paris", "keywords": "Hotels"}
    )
    assert "error" in result and "user_input_in_english is required" in result["error"]

    # Missing keywords
    result = await handlers.process_hotel_query(
        {"destination": "Paris", "user_input_in_english": "Hotels in Paris"}
    )
    assert "error" in result and "keywords is required" in result["error"]


@pytest.mark.asyncio
async def test_process_hotel_query_success(mock_client):
    mock_client.get_hotel_recommendations.return_value = {"result": "ok"}
    params = {
        "destination": "Paris",
        "user_input_in_english": "Hotels",
        "keywords": "Hotels",
    }
    result = await handlers.process_hotel_query(params)
    assert result == {"result": "ok"}
    mock_client.get_hotel_recommendations.assert_called_once_with(**params)


@pytest.mark.asyncio
async def test_process_flight_query_required_params(mock_client):
    # Missing origin
    result = await handlers.process_flight_query(
        {
            "destination": "LAX",
            "user_input_in_english": "Flights to LA",
            "keywords": "Flights",
        }
    )
    assert "error" in result and "Origin is required" in result["error"]

    # Missing destination
    result = await handlers.process_flight_query(
        {
            "origin": "JFK",
            "user_input_in_english": "Flights to LA",
            "keywords": "Flights",
        }
    )
    assert "error" in result and "Destination is required" in result["error"]

    # Missing user_input_in_english
    result = await handlers.process_flight_query(
        {"origin": "JFK", "destination": "LAX", "keywords": "Flights"}
    )
    assert "error" in result and "user_input_in_english is required" in result["error"]

    # Missing keywords
    result = await handlers.process_flight_query(
        {"origin": "JFK", "destination": "LAX", "user_input_in_english": "Flights"}
    )
    assert "error" in result and "keywords is required" in result["error"]


@pytest.mark.asyncio
async def test_process_flight_query_success(mock_client):
    mock_client.get_flight_recommendations.return_value = {"result": "ok"}
    params = {
        "origin": "JFK",
        "destination": "LAX",
        "user_input_in_english": "Flights",
        "keywords": "Flights",
    }
    result = await handlers.process_flight_query(params)
    assert result == {"result": "ok"}
    mock_client.get_flight_recommendations.assert_called_once_with(**params)


@pytest.mark.asyncio
async def test_process_activity_query_required_params(mock_client):
    # Missing destination
    result = await handlers.process_activity_query(
        {"user_input_in_english": "Things to do in Paris", "keywords": "Activities"}
    )
    assert "error" in result and "Destination is required" in result["error"]

    # Missing user_input_in_english
    result = await handlers.process_activity_query(
        {"destination": "Paris", "keywords": "Activities"}
    )
    assert "error" in result and "user_input_in_english is required" in result["error"]

    # Missing keywords
    result = await handlers.process_activity_query(
        {"destination": "Paris", "user_input_in_english": "Things to do"}
    )
    assert "error" in result and "keywords is required" in result["error"]


@pytest.mark.asyncio
async def test_process_activity_query_success(mock_client):
    mock_client.get_activity_recommendations.return_value = {"result": "ok"}
    params = {
        "destination": "Paris",
        "user_input_in_english": "Things to do",
        "keywords": "Activities",
    }
    result = await handlers.process_activity_query(params)
    assert result == {"result": "ok"}
    mock_client.get_activity_recommendations.assert_called_once_with(**params)


@pytest.mark.asyncio
async def test_process_car_query_required_params(mock_client):
    # Missing pickup_location
    result = await handlers.process_car_query(
        {"user_input_in_english": "Car rental", "keywords": "CarRental"}
    )
    assert "error" in result and "Pickup location is required" in result["error"]

    # Missing user_input_in_english
    result = await handlers.process_car_query(
        {"pickup_location": "LAX", "keywords": "CarRental"}
    )
    assert "error" in result and "user_input_in_english is required" in result["error"]

    # Missing keywords
    result = await handlers.process_car_query(
        {"pickup_location": "LAX", "user_input_in_english": "Car rental"}
    )
    assert "error" in result and "keywords is required" in result["error"]


@pytest.mark.asyncio
async def test_process_car_query_success(mock_client):
    mock_client.get_car_recommendations.return_value = {"result": "ok"}
    params = {
        "pickup_location": "LAX",
        "user_input_in_english": "Car rental",
        "keywords": "CarRental",
    }
    result = await handlers.process_car_query(params)
    assert result == {"result": "ok"}
    mock_client.get_car_recommendations.assert_called_once_with(**params)
