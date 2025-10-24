from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
USER_AGENT = "weather-app/1.0"


# TODO: get_forecast()
# Retrieves the forecast for the specified location, with an optional argument for the range of the forecast


# TODO: get_location()
# Uses the Open-Meteo Geocoding API for more accurate location searches (without this you are relying on the LLM to generate the latitude and longitude, which can result in errors)


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Get current weather for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"

    data = await make_openmeteo_request(url)

    if not data:
        return "Unable to fetch current weather data for this location."
    
    return data


async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            # Guard against errors in MCP Inspcetor (and maybe elsewhere?) like
            # "validation error for get_current_weatherOutput ... Input should be a valid string"
            return json.dumps(response.json())
        except Exception:
            return None

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
