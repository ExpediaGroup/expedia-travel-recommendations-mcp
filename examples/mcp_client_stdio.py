import os
import json
import asyncio
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession


async def main():
    # Prompt for the API key
    api_key = input("🔑 Enter your EXPEDIA_API_KEY: ").strip()

    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "-m",
            "expedia_travel_recommendations.main",
            "--protocol",
            "stdio",
        ],
        env={**os.environ, "EXPEDIA_API_KEY": api_key},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("\n🚀 Initializing session...")
            await session.initialize()

            tools = await session.list_tools()
            print("\n🧰 Available Tools:\n")
            for tool in tools.tools:
                print(f"🔹 {tool.name} - {tool.description.strip().splitlines()[0]}")

            result = await session.call_tool(
                "get_hotel_recommendations",
                arguments={
                    "query": {"destination": "Seattle"},
                    "user_input_in_english": "hotels in seattle",
                    "keywords": "hotel|seattle",
                },
            )

            print("\n🏨 Hotel Recommendations:\n")

            # Extract the JSON string from the response and parse it
            content_str = result.content[0].text
            try:
                parsed = json.loads(content_str)
                print(json.dumps(parsed["data"], indent=2))
            except Exception as e:
                print("❌ Failed to parse hotel results")
                print(e)
                print(content_str)


if __name__ == "__main__":
    asyncio.run(main())
