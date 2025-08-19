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

import asyncio
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
import json


async def getHotels():
    """
    Connects to a FastMCP server via Streamable HTTP,
    pings it, lists available tools, and calls a hotel recommendation tool.
    """
    # 1. Define the transport: How the client will connect to the server.
    #    This points to the server's HTTP endpoint.
    transport = StreamableHttpTransport("http://localhost:9900/mcp/")

    # 2. Establish a client connection within an async context.
    #    The 'async with' ensures the connection is properly opened and closed.
    async with Client(transport=transport) as client:
        # 3. Ping the server to check connectivity.
        await client.ping()
        print("Ping successful!")

        # 4. List available tools on the server.
        #    This is useful for discovery and debugging.
        await client.list_tools()
        # print("Available Tools:", tools)

        # 5. Call a specific tool on the server.
        #    'get_hotel_recommendations' is the tool name defined on your MCP server.
        #    The dictionary contains the arguments for that tool.
        res = await client.call_tool(
            "get_hotel_recommendations",
            {
                "query": {"destination": "Seattle"},
                "user_input_in_english": "hotels in seattle",
                "keywords": "hotel|seattle",
            },
        )
        # 6. Print the response received from the tool call.
        json_text = res[0].text
        data = json.loads(json_text)

        hotels = data["data"]

        for hotel in hotels:
            print(f"🏨 {hotel['hotel_name']}")
            print(hotel["description"])
            print("📍", hotel["location_description"])
            print(
                f"⭐ {hotel['star_rating']} stars, Guest rating: {hotel['guest_rating']} ({hotel['guest_review_count']} reviews)"
            )
            print(
                f"💲 Avg nightly price: {hotel['avg_nightly_price']} {hotel['currency']}"
            )
            print(
                f"📅 Check-in: {hotel['checkin_date']} → Check-out: {hotel['checkout_date']}"
            )
            print(f"🔗 [Book here]({hotel['url']})")
            print(f"🖼 Preview photo: {hotel['preview_photo']}")
            print("\n---\n")


if __name__ == "__main__":
    # Run the asynchronous client function.
    asyncio.run(getHotels())
