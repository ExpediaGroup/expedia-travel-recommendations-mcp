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

import os
import logging
import base64
from typing import Dict, Any
import requests
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ExpediaApiClient:
    """Client for interacting with Expedia Travel Recommendation Service API."""

    def __init__(self):
        self.api_key = os.getenv("EXPEDIA_API_KEY")
        if not self.api_key:
            logger.warning("EXPEDIA_API_KEY not found in environment variables")

        # Use the correct base URL from the OpenAPI spec
        self.base_url = "https://apim.expedia.com"

        # Authentication headers based on Expedia API requirements
        self.headers = {
            # Method 1: Standard API key in header
            "X-API-KEY": self.api_key,
            # Method 2: Authorization header with Basic token
            "Authorization": f"Basic {self.api_key}",
            # Common headers for JSON APIs
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Expedia API.

        Args:
            endpoint: API endpoint path
            params: Query parameters for the request

        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}{endpoint}"

        # Ensure user_input_in_english and keywords are included in params
        if "user_input_in_english" not in params:
            logger.warning(
                "user_input_in_english is missing from API request parameters"
            )

        if "keywords" not in params:
            logger.warning("keywords is missing from API request parameters")

        try:
            logger.info(f"Making request to: {url}")
            logger.info(f"Request parameters: {params}")
            logger.info(f"Request headers: {self.headers}")
            # Attempt request
            response = requests.get(url, headers=self.headers, params=params)

            # Log the response status and details for debugging
            logger.info(f"Response status: {response.status_code}")

            # If we get an unauthorized error, try with basic auth
            if response.status_code == 401:
                logger.info("Trying with Basic Auth fallback")
                # Using API key as both username and password as a fallback
                basic_auth_headers = self.headers.copy()
                auth_str = base64.b64encode(
                    f"{self.api_key}:{self.api_key}".encode()
                ).decode()
                basic_auth_headers["Authorization"] = f"Basic {auth_str}"

                response = requests.get(url, headers=basic_auth_headers, params=params)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            # Include more details about the error for debugging
            error_details = {
                "error": str(e),
                "url": url,
                "params": params,
                "response": (
                    getattr(e.response, "text", "No response text")
                    if hasattr(e, "response")
                    else "No response"
                ),
            }
            return error_details

    def get_hotel_recommendations(self, **params) -> Dict[str, Any]:
        """Get hotel recommendations based on the provided parameters."""
        # Use the correct endpoint from the OpenAPI spec
        endpoint = "/recommendations/hotels"
        return self._make_request(endpoint, params)

    def get_flight_recommendations(self, **params) -> Dict[str, Any]:
        """Get flight recommendations based on the provided parameters."""
        # Use the correct endpoint from the OpenAPI spec
        endpoint = "/recommendations/flights"
        return self._make_request(endpoint, params)

    def get_activity_recommendations(self, **params) -> Dict[str, Any]:
        """Get activity recommendations based on the provided parameters."""
        # Use the correct endpoint from the OpenAPI spec
        endpoint = "/recommendations/activities"
        return self._make_request(endpoint, params)

    def get_car_recommendations(self, **params) -> Dict[str, Any]:
        """Get car rental recommendations based on the provided parameters."""
        # Use the correct endpoint from the OpenAPI spec
        endpoint = "/recommendations/cars"
        return self._make_request(endpoint, params)
