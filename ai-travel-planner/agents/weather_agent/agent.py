import os
from google.adk import Agent
from google.genai import types
import httpx
import json

# Task 5: Build Weather Agent

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


# --- Tool Function ---
async def get_weather(location: str) -> str:
    """
    Fetches the 5-day weather forecast (40 items, typically) from OpenWeatherMap
    for a given city/location using the current API key.

    Args:
        location: The name of the city or location (e.g., "Paris, France").

    Returns:
        A human-readable string summarizing the key weather details.
    """
    if not OPENWEATHERMAP_API_KEY:
        return "Error: OpenWeatherMap API key is not configured."

    # Use an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        # NOTE: OpenWeatherMap free tier only gives 5-day/3-hour forecasts (40 data points).
        # We process the raw data to extract daily highs/lows for a simplified daily summary.
        params = {
            "q": location,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric",  # Use Celsius
        }

        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            return f"Error retrieving weather data: API returned status code {e.response.status_code}."
        except httpx.RequestError as e:
            return f"Error connecting to OpenWeatherMap API: {e}."
        except json.JSONDecodeError:
            return "Error: Received unreadable response from the weather service."

    # --- Data Processing (Converting 3-hour forecasts to a daily summary) ---
    daily_forecasts = {}

    for item in data.get("list", []):
        # The dt_txt is in 'YYYY-MM-DD HH:MM:SS' format
        date_str = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        weather_description = item["weather"][0]["description"]

        if date_str not in daily_forecasts:
            # Initialize with first temperature as min/max
            daily_forecasts[date_str] = {
                "min_temp": temp,
                "max_temp": temp,
                "weather": weather_description,
                "count": 1,
            }
        else:
            # Update min/max temperatures
            daily_forecasts[date_str]["min_temp"] = min(
                daily_forecasts[date_str]["min_temp"], temp
            )
            daily_forecasts[date_str]["max_temp"] = max(
                daily_forecasts[date_str]["max_temp"], temp
            )
            # Simplistic way to get the "main" weather for the day (last update wins)
            daily_forecasts[date_str]["weather"] = weather_description
            daily_forecasts[date_str]["count"] += 1

    summary = []
    for date, daily_data in daily_forecasts.items():
        summary.append(
            f"{date}: {daily_data['weather'].capitalize()} (High: {daily_data['max_temp']:.1f}°C, Low: {daily_data['min_temp']:.1f}°C)"
        )

    if not summary:
        return f"Could not find a forecast for {location}. Please check the location spelling."

    return f"Multiday Weather Forecast for {location}:\n- " + "\n- ".join(summary)


# --- Agent Definition ---
root_agent = Agent(
    model="gemini-2.5-flash",
    name="weather_agent",
    description="Provides weather forecasts for a destination using OpenWeatherMap.",
    instruction="Answer weather-related questions using the get_weather tool. If the learner does not specifies the number of days for forecast, you'll usually respond with the forecast for the next 5 days.",
    tools=[get_weather],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
