from typing import Any
import httpx
import json
from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_forecast(latitude: float, longitude: float, days: int = 7) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        days: Number of days to forecast (1-16, default is 7)
    
    Returns:
        JSON string with daily weather forecast
    """
    # Validate days parameter
    if days < 1:
        days = 1
    elif days > 16:
        days = 16
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code,sunrise,sunset,uv_index_max&forecast_days={days}&timezone=auto"
    data = await make_openmeteo_request(url)
    if not data:
        return "Unable to fetch forecast data for this location."
    return data


@mcp.tool()
async def get_location(location: str) -> str:
    """Search for a location and get its coordinates using the Open-Meteo Geocoding API.

    Args:
        location: Name of the location to search for (e.g., "New York", "London", "Tokyo")

    Returns:
        JSON string with location details including name, country, latitude, longitude, and other info
    """
    # Handle special characters and spaces in the location
    location = quote(location)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=5&language=en&format=json"
    data = await make_openmeteo_request(url)
    if not data:
        return "Unable to fetch location data. Please try a different location name."
    return data


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Get current weather for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"
    data = await make_openmeteo_request(url)
    if not data:
        return "Unable to fetch current weather data for this location."
    return data


async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API with proper error handling."""
    headers = {
        "User-Agent": "weather-app/1.0",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            # Guard against errors in MCP Inspcetor (and maybe elsewhere?) like
            # "validation error for get_current_weatherOutput ... Input should be a valid string"
            return json.dumps(response.json())
        except Exception as e:
            return f'Error: {str(e)}'

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
