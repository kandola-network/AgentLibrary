from fastapi import FastAPI, HTTPException
import requests
import os
import dotenv

dotenv.load_dotenv()

app = FastAPI()

# API Keys
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY","cb965d906375733a72c8e36b1a3d610f")
FORECAST_API_KEY = os.getenv("FORECAST_API_KEY","frtdAy8Jp8UgMT2fTYvhXgkBoE7vlyvz")

# Routes

@app.get("/weather/current", tags=["Weather"])
def get_current_weather(location: str):
    """
    Get the current weather for a location.
    :param location: The location to get the weather for.
    :return: JSON with the current weather information.
    """
    url = "http://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": location}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error: Unable to fetch current weather data for {location}."
        )
    
    data = response.json()
    if "current" not in data:
        raise HTTPException(
            status_code=404,
            detail=f"No weather data found for {location}."
        )
    
    current_weather = data["current"]
    return {
        "location": location,
        "temperature": current_weather.get("temperature", "N/A"),
        "description": current_weather.get("weather_descriptions", ["N/A"])[0],
        "humidity": current_weather.get("humidity", "N/A"),
        "wind_speed": current_weather.get("wind_speed", "N/A"),
    }

@app.get("/weather/forecast", tags=["Weather"])
def get_weather_forecast(location: str):
    """
    Get the weather forecast for a location.
    :param location: The location to get the weather forecast for.
    :return: JSON with the weather forecast information.
    """
    url = f"https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": location,
        "apikey": FORECAST_API_KEY,
    }
    
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error: Unable to fetch weather forecast for {location}."
        )
    
    forecast_data = response.json()
    return {
        "location": location,
        "forecast": forecast_data,  # You can structure this further as per your requirements.
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8001)
