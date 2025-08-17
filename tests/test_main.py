import pytest
from unittest.mock import AsyncMock, patch
from fastmcp import Context
from expedia_travel_recommendations.main import (
    get_hotel_recommendations,
    get_flight_recommendations,
    get_activity_recommendations,
    get_car_recommendations,
    mcp,
)


@pytest.mark.asyncio
async def test_get_hotel_recommendations_required_params():
    ctx = Context(mcp)
    with patch(
        "expedia_travel_recommendations.main.process_hotel_query",
        new_callable=AsyncMock,
    ) as mock_process:
        mock_process.return_value = {"hotels": ["Hotel A", "Hotel B"]}
        result = await get_hotel_recommendations(destination="Paris", ctx=ctx)
        assert "error" not in result
        assert result["hotels"] == ["Hotel A", "Hotel B"]


@pytest.mark.asyncio
async def test_get_flight_recommendations_required_params():
    ctx = Context(mcp)
    with patch(
        "expedia_travel_recommendations.main.process_flight_query",
        new_callable=AsyncMock,
    ) as mock_process:
        mock_process.return_value = {"flights": ["Flight X", "Flight Y"]}
        result = await get_flight_recommendations(
            origin="JFK", destination="LAX", ctx=ctx
        )
        assert "error" not in result
        assert result["flights"] == ["Flight X", "Flight Y"]


@pytest.mark.asyncio
async def test_get_activity_recommendations_required_params():
    ctx = Context(mcp)
    with patch(
        "expedia_travel_recommendations.main.process_activity_query",
        new_callable=AsyncMock,
    ) as mock_process:
        mock_process.return_value = {"activities": ["Museum Visit", "City Tour"]}
        result = await get_activity_recommendations(destination="Paris", ctx=ctx)
        assert "error" not in result
        assert result["activities"] == ["Museum Visit", "City Tour"]


@pytest.mark.asyncio
async def test_get_car_recommendations_required_params():
    ctx = Context(mcp)
    with patch(
        "expedia_travel_recommendations.main.process_car_query", new_callable=AsyncMock
    ) as mock_process:
        mock_process.return_value = {"cars": ["Sedan", "SUV"]}
        result = await get_car_recommendations(pickup_location="JFK", ctx=ctx)
        assert "error" not in result
        assert result["cars"] == ["Sedan", "SUV"]
