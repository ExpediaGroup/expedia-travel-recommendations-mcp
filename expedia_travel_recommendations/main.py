#!/usr/bin/env python3
"""
Copyright [2025] Expedia, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Expedia Travel Recommendation Service MCP Server

This MCP server provides an interface to the Expedia Travel Recommendation Service API,
supporting both stdio and http-sse protocols.
"""
import logging
import argparse
from typing import Dict, Any

from dotenv import load_dotenv
from fastmcp import FastMCP, Context

from expedia_travel_recommendations.api.handlers import (
    process_hotel_query,
    process_flight_query,
    process_activity_query,
    process_car_query,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP(title="Expedia Travel Recommendation MCP Server")


@mcp.tool()
async def get_hotel_recommendations(
    destination: str,
    check_in: str = None,
    check_out: str = None,
    property_types: list = None,
    number_of_travelers: int = None,
    min_bedrooms: int = None,
    amenities: list = None,
    guest_rating: float = None,
    star_ratings: list = None,
    sort_type: str = None,
    distance: float = None,
    query_text: str = "",
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Get hotel recommendations based on provided parameters.

    Args:
        destination: (required) The destination for the hotel search
        check_in: (optional) Check-in date in YYYY-MM-DD format
        check_out: (optional) Check-out date in YYYY-MM-DD format
        property_types: (optional) List of property types (e.g., HOTEL, RESORT)
        number_of_travelers: (optional) Number of travelers
        min_bedrooms: (optional) Minimum number of bedrooms
        amenities: (optional) List of required amenities (e.g., POOL, SPA)
        guest_rating: (optional) Minimum guest rating
        star_ratings: (optional) List of star ratings
        sort_type: (optional) Type of sorting (e.g., CHEAPEST, BEST_REVIEWED)
        distance: (optional) Maximum distance from destination center
        query_text: Original user's query in natural language
        ctx: Context object for logging
    """
    try:
        if not destination:
            return {"error": "Destination is required"}

        # Build query dictionary only with available parameters
        query_with_required_params = {
            "destination": destination,
            "user_input_in_english": query_text,
            "keywords": "Hotels|MCP",
        }

        optional_params = {
            "check_in": check_in,
            "check_out": check_out,
            "property_types": property_types,
            "number_of_travelers": number_of_travelers,
            "min_bedrooms": min_bedrooms,
            "amenities": amenities,
            "guest_rating": guest_rating,
            "star_ratings": star_ratings,
            "sort_type": sort_type,
            "distance": distance,
        }
        # Add only non-None values
        query_with_required_params.update(
            {k: v for k, v in optional_params.items() if v is not None}
        )

        ctx.info(f"Processing hotel recommendation request for {destination}")
        ctx.info(f"User input: {query_text}")

        result = await process_hotel_query(query_with_required_params)

        if "error" in result:
            ctx.error(f"Error in hotel recommendations: {result['error']}")
            return {"error": result["error"]}

        ctx.info("Successfully retrieved hotel recommendations")
        return result

    except Exception as e:
        ctx.error(f"Exception in hotel recommendations: {e}")
        return {"error": str(e)}


@mcp.tool()
async def get_flight_recommendations(
    origin: str,
    destination: str,
    departure_date: str = None,
    airline_code: str = None,
    number_of_stops: int = None,
    sort_type: str = None,
    query_text: str = "",
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Get flight recommendations based on provided parameters.

    Args:
        origin: (required) Origin airport or city code
        destination: (required) Destination airport or city code
        departure_date: (optional) Departure date in YYYY-MM-DD format
        airline_code: (optional) Preferred airline code
        number_of_stops: (optional) Maximum number of stops
        sort_type: (optional) Type of sorting (e.g., CHEAPEST, SHORTEST)
        query_text: Original user's query in natural language
        ctx: Context object for logging
    """
    try:
        if not origin or not destination:
            return {"error": "Both origin and destination are required"}

        # Build query dictionary dynamically from provided params
        query_with_required_params = {
            "origin": origin,
            "destination": destination,
            "user_input_in_english": query_text,
            "keywords": "Flights|MCP",
        }

        optional_params = {
            "departure_date": departure_date,
            "airline_code": airline_code,
            "number_of_stops": number_of_stops,
            "sort_type": sort_type,
        }

        # Include only non-None optional params
        query_with_required_params.update(
            {k: v for k, v in optional_params.items() if v is not None}
        )

        ctx.info(
            f"Processing flight recommendation request from {origin} to {destination}"
        )
        ctx.info(f"User input: {query_text}")

        result = await process_flight_query(query_with_required_params)

        if "error" in result:
            ctx.error(f"Error in flight recommendations: {result['error']}")
            return {"error": result["error"]}

        ctx.info("Successfully retrieved flight recommendations")
        return result

    except Exception as e:
        ctx.error(f"Exception in flight recommendations: {e}")
        return {"error": str(e)}


@mcp.tool()
async def get_activity_recommendations(
    destination: str,
    start_date: str = None,
    end_date: str = None,
    categories: list = None,
    duration: int = None,
    price_max: float = None,
    query_text: str = "",
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Get activity recommendations based on the provided parameters.

    Args:
        destination: (required) The destination for the activity search
        start_date: (optional) Start date in YYYY-MM-DD format
        end_date: (optional) End date in YYYY-MM-DD format
        categories: (optional) List of activity categories
        duration: (optional) Maximum activity duration in hours
        price_max: (optional) Maximum price
        query_text: Original user's query in natural language
        ctx: Context object for logging
    """
    try:
        if not destination:
            return {"error": "Destination is required"}

        # Build query dictionary dynamically
        query_with_required_params = {
            "destination": destination,
            "user_input_in_english": query_text,
            "keywords": "Activities|MCP",
        }

        optional_params = {
            "start_date": start_date,
            "end_date": end_date,
            "categories": categories,
            "duration": duration,
            "price_max": price_max,
        }

        # Add only params that are not None
        query_with_required_params.update(
            {k: v for k, v in optional_params.items() if v is not None}
        )

        ctx.info(f"Processing activity recommendation request for {destination}")
        ctx.info(f"User input: {query_text}")

        result = await process_activity_query(query_with_required_params)

        if "error" in result:
            ctx.error(f"Error in activity recommendations: {result['error']}")
            return {"error": result["error"]}

        ctx.info("Successfully retrieved activity recommendations")
        return result

    except Exception as e:
        ctx.error(f"Exception in activity recommendations: {e}")
        return {"error": str(e)}


@mcp.tool()
async def get_car_recommendations(
    pickup_location: str,
    dropoff_location: str = None,
    pickup_date: str = None,
    pickup_time: str = None,
    dropoff_date: str = None,
    dropoff_time: str = None,
    car_classes: list = None,
    query_text: str = "",
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Get car rental recommendations based on the provided parameters.

    Args:
        pickup_location: (required) Pickup location
        dropoff_location: (optional) Dropoff location
        pickup_date: (optional) Pickup date in YYYY-MM-DD format
        pickup_time: (optional) Pickup time in HH:MM format
        dropoff_date: (optional) Dropoff date in YYYY-MM-DD format
        dropoff_time: (optional) Dropoff time in HH:MM format
        car_classes: (optional) List of car classes
        query_text: Original user's query in natural language
        ctx: Context object for logging
    """
    try:
        if not pickup_location:
            return {"error": "Pickup location is required"}

        # Build query dictionary dynamically
        query_with_required_params = {
            "pickup_location": pickup_location,
            "user_input_in_english": query_text,
            "keywords": "CarRental|MCP",
        }

        optional_params = {
            "dropoff_location": dropoff_location,
            "pickup_date": pickup_date,
            "pickup_time": pickup_time,
            "dropoff_date": dropoff_date,
            "dropoff_time": dropoff_time,
            "car_classes": car_classes,
        }

        # Add only non-None optional params
        query_with_required_params.update(
            {k: v for k, v in optional_params.items() if v is not None}
        )

        ctx.info(
            f"Processing car recommendation request for pickup at {pickup_location}"
        )
        ctx.info(f"User input: {query_text}")

        result = await process_car_query(query_with_required_params)

        if "error" in result:
            ctx.error(f"Error in car recommendations: {result['error']}")
            return {"error": result["error"]}

        ctx.info("Successfully retrieved car recommendations")
        return result

    except Exception as e:
        ctx.error(f"Exception in car recommendations: {e}")
        return {"error": str(e)}


def main():
    """Run the MCP server with the specified protocol."""
    parser = argparse.ArgumentParser(
        description="Expedia Travel Recommendation MCP Server"
    )
    parser.add_argument(
        "--protocol",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Protocol to use (stdio or streamable-http)",
    )
    parser.add_argument(
        "--port",
        default="9900",
        type=int,
        help="Protocol to use (stdio or streamable-http)",
    )
    args = parser.parse_args()

    if args.protocol == "stdio":
        # Run with stdio protocol
        mcp.run()
    else:
        # Run with http-sse protocol
        mcp.run(transport="streamable-http", port=args.port)


if __name__ == "__main__":
    main()
