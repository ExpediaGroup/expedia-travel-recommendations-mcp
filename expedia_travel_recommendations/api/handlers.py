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
"""

import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv
from expedia_travel_recommendations.api.client import ExpediaApiClient

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Determine whether to use the mock client (default to False for production)
USE_MOCK_CLIENT = os.getenv("USE_MOCK_CLIENT", "false").lower() == "true"

logger.info("Using Expedia API client")
api_client = ExpediaApiClient()


async def process_hotel_query(user_query: Dict[str, Any]) -> Dict[str, Any]:
    """Process a hotel recommendation query."""
    try:
        # Extract parameters from user query
        params = {}

        # Simply pass through all parameters from the query
        params = user_query.copy()

        # Required parameter check
        if "destination" not in params:
            return {"error": "Destination is required for hotel recommendations"}

        # Mandatory parameters check
        if "user_input_in_english" not in params:
            return {
                "error": "user_input_in_english is required for hotel recommendations"
            }

        if "keywords" not in params:
            return {"error": "keywords is required for hotel recommendations"}

        # Call the API
        logger.info(f"Calling hotel recommendations API with params: {params}")
        return api_client.get_hotel_recommendations(**params)

    except Exception as e:
        logger.error(f"Error processing hotel query: {e}")
        return {"error": str(e)}


async def process_flight_query(user_query: Dict[str, Any]) -> Dict[str, Any]:
    """Process a flight recommendation query."""
    try:
        # Simply pass through all parameters from the query
        params = user_query.copy()

        # Required parameters check
        if "origin" not in params:
            return {"error": "Origin is required for flight recommendations"}

        if "destination" not in params:
            return {"error": "Destination is required for flight recommendations"}

        # Mandatory parameters check
        if "user_input_in_english" not in params:
            return {
                "error": "user_input_in_english is required for flight recommendations"
            }

        if "keywords" not in params:
            return {"error": "keywords is required for flight recommendations"}

        # Call the API
        logger.info(f"Calling flight recommendations API with params: {params}")
        return api_client.get_flight_recommendations(**params)

    except Exception as e:
        logger.error(f"Error processing flight query: {e}")
        return {"error": str(e)}


async def process_activity_query(user_query: Dict[str, Any]) -> Dict[str, Any]:
    """Process an activity recommendation query."""
    try:
        # Simply pass through all parameters from the query
        params = user_query.copy()

        # Required parameter check
        if "destination" not in params:
            return {"error": "Destination is required for activity recommendations"}

        # Mandatory parameters check
        if "user_input_in_english" not in params:
            return {
                "error": "user_input_in_english is required for activity recommendations"
            }

        if "keywords" not in params:
            return {"error": "keywords is required for activity recommendations"}

        # Call the API
        logger.info(f"Calling activity recommendations API with params: {params}")
        return api_client.get_activity_recommendations(**params)

    except Exception as e:
        logger.error(f"Error processing activity query: {e}")
        return {"error": str(e)}


async def process_car_query(user_query: Dict[str, Any]) -> Dict[str, Any]:
    """Process a car rental recommendation query."""
    try:
        # Simply pass through all parameters from the query
        params = user_query.copy()

        # Required parameter check
        if "pickup_location" not in params:
            return {"error": "Pickup location is required for car recommendations"}

        # Mandatory parameters check
        if "user_input_in_english" not in params:
            return {
                "error": "user_input_in_english is required for car recommendations"
            }

        if "keywords" not in params:
            return {"error": "keywords is required for car recommendations"}

        # Call the API
        logger.info(f"Calling car recommendations API with params: {params}")
        return api_client.get_car_recommendations(**params)

    except Exception as e:
        logger.error(f"Error processing car query: {e}")
        return {"error": str(e)}
