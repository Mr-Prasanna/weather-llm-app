# # import requests
# # import os
# # import json
# # from dotenv import load_dotenv
# # from langchain.tools import tool

# # load_dotenv()

# # WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
# # BASE_URL = "https://api.openweathermap.org/data/2.5"


# # # def get_weather(city: str, units: str = "metric") -> dict:
# # #     """
# # #     Raw function — fetches weather from OpenWeatherMap API.
# # #     Returns a clean structured dict.
# # #     """
# # #     current_resp = requests.get(
# # #         f"{BASE_URL}/weather",
# # #         params={
# # #             "q": city,
# # #             "appid": WEATHER_API_KEY,
# # #             "units": units
# # #         }
# # #     )

# # #     if current_resp.status_code != 200:
# # #         return {"error": f"City '{city}' not found. Please check the city name."}

# # #     current_data = current_resp.json()

# # #     forecast_resp = requests.get(
# # #         f"{BASE_URL}/forecast",
# # #         params={
# # #             "q": city,
# # #             "appid": WEATHER_API_KEY,
# # #             "units": units
# # #         }
# # #     )

# # #     forecast_data = forecast_resp.json()

# # #     daily_forecasts = []
# # #     seen_dates = set()

# # #     for item in forecast_data["list"]:
# # #         date = item["dt_txt"].split(" ")[0]
# # #         time = item["dt_txt"].split(" ")[1]

# # #         if date not in seen_dates and time == "12:00:00":
# # #             seen_dates.add(date)
# # #             daily_forecasts.append({
# # #                 "date": date,
# # #                 "temp": item["main"]["temp"],
# # #                 "feels_like": item["main"]["feels_like"],
# # #                 "humidity": item["main"]["humidity"],
# # #                 "description": item["weather"][0]["description"],
# # #                 "wind_speed": item["wind"]["speed"]
# # #             })

# # #     unit_symbol = "\u00b0C" if units == "metric" else "\u00b0F"

# # #     result = {
# # #         "city": current_data["name"],
# # #         "country": current_data["sys"]["country"],
# # #         "current": {
# # #             "temp": f"{current_data['main']['temp']}{unit_symbol}",
# # #             "feels_like": f"{current_data['main']['feels_like']}{unit_symbol}",
# # #             "humidity": f"{current_data['main']['humidity']}%",
# # #             "description": current_data["weather"][0]["description"],
# # #             "wind_speed": f"{current_data['wind']['speed']} m/s",
# # #         },
# # #         "forecast": daily_forecasts,
# # #         "units": units
# # #     }

# # #     return result

# # # def get_weather(city: str, units: str = "metric") -> dict:
    
# # #     # Clean city name — remove extra spaces and special characters
# # #     city = city.strip().strip("?.,!")
    
# # #     current_resp = requests.get(
# # #         f"{BASE_URL}/weather",
# # #         params={
# # #             "q": city,
# # #             "appid": WEATHER_API_KEY,
# # #             "units": units
# # #         }
# # #     )

# # #     if current_resp.status_code != 200:
# # #         return {"error": f"City '{city}' not found. Please check the city name."}
    
# # def get_weather(city: str, units: str = "metric") -> dict:
    
# #     # Clean city name
# #     city = city.strip().strip("?.,!\"'")
# #     print(f"DEBUG: Fetching weather for city = '{city}'")
    
# #     current_resp = requests.get(
# #         f"{BASE_URL}/weather",
# #         params={
# #             "q": city,
# #             "appid": WEATHER_API_KEY,
# #             "units": units
# #         }
# #     )
# #     print(f"DEBUG: Status code = {current_resp.status_code}")
    
# #     if current_resp.status_code != 200:
# #         return {"error": f"City '{city}' not found. Please check the city name."}    


# # @tool
# # def weather_tool(city: str) -> str:
# #     """
# #     Use this tool to get the current weather and 5-day forecast
# #     for any city. Input should be a city name like 'London' or 'Chennai'.
# #     Returns temperature, humidity, wind speed and forecast data.
# #     """
# #     result = get_weather(city)

# #     if "error" in result:
# #         return result["error"]

# #     return json.dumps(result, indent=2)


# # # ── Test both functions ──────────────────────────────────────────────
# # if __name__ == "__main__":

# #     # Test 1 — raw function
# #     print("=== Raw Function Test ===")
# #     data = get_weather("Chennai")
# #     print(json.dumps(data, indent=2))

# #     # Test 2 — LangChain tool
# #     print("\n=== LangChain Tool Test ===")
# #     result = weather_tool.invoke({"city": "Chennai"})
# #     print(result)

# import requests
# import os
# import json
# from dotenv import load_dotenv
# from langchain_core.tools import tool

# load_dotenv()

# WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
# BASE_URL = "https://api.openweathermap.org/data/2.5"

# CITY_CORRECTIONS = {
#     "bombay": "Mumbai",
#     "madras": "Chennai",
#     "calcutta": "Kolkata",
#     "bangalore": "Bengaluru",
# }

# def clean_city(city: str) -> str:
#     city = city.strip().strip("?.,!\"'").strip()
#     if city.lower() in CITY_CORRECTIONS:
#         city = CITY_CORRECTIONS[city.lower()]
#     return city


# def get_weather(city: str, units: str = "metric") -> dict:
#     city = clean_city(city)

#     current_resp = requests.get(
#         f"{BASE_URL}/weather",
#         params={
#             "q": city,
#             "appid": WEATHER_API_KEY,
#             "units": units
#         }
#     )

#     if current_resp.status_code != 200:
#         current_resp = requests.get(
#             f"{BASE_URL}/weather",
#             params={
#                 "q": f"{city},IN",
#                 "appid": WEATHER_API_KEY,
#                 "units": units
#             }
#         )
#         if current_resp.status_code != 200:
#             return {"error": f"City '{city}' not found. Please check the city name."}

#     current_data = current_resp.json()

#     forecast_resp = requests.get(
#         f"{BASE_URL}/forecast",
#         params={
#             "q": city,
#             "appid": WEATHER_API_KEY,
#             "units": units
#         }
#     )

#     forecast_data = forecast_resp.json()
#     daily_forecasts = []
#     seen_dates = set()

#     for item in forecast_data["list"]:
#         date = item["dt_txt"].split(" ")[0]
#         time = item["dt_txt"].split(" ")[1]
#         if date not in seen_dates and time == "12:00:00":
#             seen_dates.add(date)
#             daily_forecasts.append({
#                 "date": date,
#                 "temp": item["main"]["temp"],
#                 "feels_like": item["main"]["feels_like"],
#                 "humidity": item["main"]["humidity"],
#                 "description": item["weather"][0]["description"],
#                 "wind_speed": item["wind"]["speed"]
#             })

#     unit_symbol = "\u00b0C" if units == "metric" else "\u00b0F"

#     return {
#         "city": current_data["name"],
#         "country": current_data["sys"]["country"],
#         "current": {
#             "temp": f"{current_data['main']['temp']}{unit_symbol}",
#             "feels_like": f"{current_data['main']['feels_like']}{unit_symbol}",
#             "humidity": f"{current_data['main']['humidity']}%",
#             "description": current_data["weather"][0]["description"],
#             "wind_speed": f"{current_data['wind']['speed']} m/s",
#         },
#         "forecast": daily_forecasts,
#         "units": units
#     }


# @tool
# def weather_tool(city: str) -> str:
#     """
#     Use this tool to get current weather and 5-day forecast
#     for any city. Input should be a city name like London,
#     Chennai, Mumbai, Delhi, New York or Tokyo.
#     Returns temperature, humidity, wind speed and forecast.
#     """
#     city = clean_city(city)
#     result = get_weather(city)
#     if "error" in result:
#         return result["error"]
#     return json.dumps(result, indent=2)


# if __name__ == "__main__":
#     print("=== Test Mumbai ===")
#     print(json.dumps(get_weather("Mumbai"), indent=2))


import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def clean_city(city: str) -> str:
    city = city.strip().strip("?.,!\"'").strip()
    corrections = {
        "bombay": "Mumbai",
        "madras": "Chennai",
        "calcutta": "Kolkata",
        "bangalore": "Bengaluru",
    }
    return corrections.get(city.lower(), city)


def get_weather(city: str, units: str = "metric") -> dict:
    city = clean_city(city)
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    current_resp = requests.get(
        f"{BASE_URL}/weather",
        params={"q": city, "appid": api_key, "units": units}
    )

    if current_resp.status_code != 200:
        return {"error": f"City '{city}' not found. Status: {current_resp.status_code}"}

    current_data = current_resp.json()

    forecast_resp = requests.get(
        f"{BASE_URL}/forecast",
        params={"q": city, "appid": api_key, "units": units}
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

    return {
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


def get_weather_tool_fn(city: str) -> str:
    """Plain function — no @tool decorator needed."""
    city = clean_city(city)
    result = get_weather(city)
    if "error" in result:
        return result["error"]
    return json.dumps(result, indent=2)