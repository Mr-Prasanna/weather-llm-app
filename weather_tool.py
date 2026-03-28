import requests
import os
import json
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_weather(city: str, units: str = "metric") -> dict:
    """
    Raw function — fetches weather from OpenWeatherMap API.
    Returns a clean structured dict.
    """
    current_resp = requests.get(
        f"{BASE_URL}/weather",
        params={
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": units
        }
    )

    if current_resp.status_code != 200:
        return {"error": f"City '{city}' not found. Please check the city name."}

    current_data = current_resp.json()

    forecast_resp = requests.get(
        f"{BASE_URL}/forecast",
        params={
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": units
        }
    )

    forecast_data = forecast_resp.json()

    daily_forecasts = []
    seen_dates = set()

    for item in forecast_data["list"]:
        date = item["dt_txt"].split(" ")[0]
        time = item["dt_txt"].split(" ")[1]

        if date not in seen_dates and time == "12:00:00":
            seen_dates.add(date)
            daily_forecasts.append({
                "date": date,
                "temp": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "description": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"]
            })

    unit_symbol = "\u00b0C" if units == "metric" else "\u00b0F"

    result = {
        "city": current_data["name"],
        "country": current_data["sys"]["country"],
        "current": {
            "temp": f"{current_data['main']['temp']}{unit_symbol}",
            "feels_like": f"{current_data['main']['feels_like']}{unit_symbol}",
            "humidity": f"{current_data['main']['humidity']}%",
            "description": current_data["weather"][0]["description"],
            "wind_speed": f"{current_data['wind']['speed']} m/s",
        },
        "forecast": daily_forecasts,
        "units": units
    }

    return result


@tool
def weather_tool(city: str) -> str:
    """
    Use this tool to get the current weather and 5-day forecast
    for any city. Input should be a city name like 'London' or 'Chennai'.
    Returns temperature, humidity, wind speed and forecast data.
    """
    result = get_weather(city)

    if "error" in result:
        return result["error"]

    return json.dumps(result, indent=2)


# ── Test both functions ──────────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — raw function
    print("=== Raw Function Test ===")
    data = get_weather("Chennai")
    print(json.dumps(data, indent=2))

    # Test 2 — LangChain tool
    print("\n=== LangChain Tool Test ===")
    result = weather_tool.invoke({"city": "Chennai"})
    print(result)