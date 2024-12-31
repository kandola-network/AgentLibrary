import requests

def get_current_weather(location):
    """
    Get the current weather for a location.
    param location: The location to get the weather for.
    return: A string with the current weather information.
    """
    API_KEY = 'cb965d906375733a72c8e36b1a3d610f'
    url = f'http://api.weatherstack.com/current'
    params = {
        'access_key': API_KEY,
        'query': location
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        current_weather = data.get('current', {})
        temperature = current_weather.get('temperature', 'N/A')
        weather_description = current_weather.get('weather_descriptions', ['N/A'])[0]
        humidity = current_weather.get('humidity', 'N/A')
        wind_speed = current_weather.get('wind_speed', 'N/A')
        
        return f"Currently in {location}, it’s {temperature}°F with {weather_description}. Humidity is at {humidity}%, and winds are blowing at {wind_speed} mph."
    else:
        return f"Error: Could not retrieve weather data for {location}."

# Function to get weather forecast
def get_weather_forecast(location):
    """
    Get the weather forecast for a location.
    param location: The location to get the weather forecast for.
    return: A string with the weather forecast information.
    """
    url = "https://api.tomorrow.io/v4/weather/forecast?location=new%20york&apikey=frtdAy8Jp8UgMT2fTYvhXgkBoE7vlyvz"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(response.text)# Function to set up severe weather alerts (this is a placeholder, since WeatherStack does not provide an actual alert feature in the free API)

def set_severe_weather_alert(location):
    # For this example, we simulate severe weather alerts. WeatherStack doesn't provide direct alert functionality.
    return f"Severe weather alerts for {location} are enabled. You’ll be notified of any severe weather warnings."

# Example usage:
if __name__ == '__main__':
    # Get current weather
    print(get_current_weather('New York'))

    # Get weather forecast for the next 3 days
    print(get_weather_forecast('Tokyo'))

    # Set up a severe weather alert
    print(set_severe_weather_alert('Miami'))
