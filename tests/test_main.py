import pytest
from unittest.mock import AsyncMock, patch
from fastmcp import Context
from expedia_travel_recommendations.main import (
    get_hotel_recommendations,
    get_flight_recommendations,
    get_activity_recommendations,
    get_car_recommendations,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool,kind,params",
    [
        (get_hotel_recommendations, "hotel", {"destination": "Paris"}),
        (get_flight_recommendations, "flight", {"origin": "JFK", "destination": "LAX"}),
        (get_activity_recommendations, "activity", {"destination": "Paris"}),
        (get_car_recommendations, "car", {"pickup_location": "JFK"}),
    ],
)
@pytest.mark.parametrize("outcome", ["success", "error", "exception"])
async def test_context_logging_is_awaited(tool, kind, params, outcome):
    ctx = AsyncMock(spec=Context)
    with patch(
        f"expedia_travel_recommendations.main.process_{kind}_query",
        new_callable=AsyncMock,
    ) as process:
        process.return_value = (
            {"result": "ok"} if outcome == "success" else {"error": "failed"}
        )
        if outcome == "exception":
            process.side_effect = RuntimeError("failed")
        result = await tool(ctx=ctx, **params)
    assert ctx.info.await_count == (3 if outcome == "success" else 2)
    assert ctx.info.await_count == ctx.info.call_count
    if outcome == "success":
        assert result == {"result": "ok"}
        ctx.error.assert_not_called()
    else:
        assert "error" in result
        ctx.error.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_hotel_recommendations_required_params():
    ctx = AsyncMock(spec=Context)
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
    ctx = AsyncMock(spec=Context)
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
    ctx = AsyncMock(spec=Context)
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
    ctx = AsyncMock(spec=Context)
    with patch(
        "expedia_travel_recommendations.main.process_car_query", new_callable=AsyncMock
    ) as mock_process:
        mock_process.return_value = {"cars": ["Sedan", "SUV"]}
        result = await get_car_recommendations(pickup_location="JFK", ctx=ctx)
        assert "error" not in result
        assert result["cars"] == ["Sedan", "SUV"]
