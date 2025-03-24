import requests
import pandas as pd

def fetch_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()

    # Extract and clean temperature data
    temperature = data['current'].get('temp', None)  # Handle missing 'temp'
    if temperature is None:
        temperature = 0.0  # Default value for missing temperature
    else:
        temperature = round(temperature, 2)  # Round to 2 decimal places

    # Extract and clean humidity data
    humidity = data['current'].get('humidity', None)  # Handle missing 'humidity'
    if humidity is None:
        humidity = 0  # Default value for missing humidity

    # Extract and clean pressure data
    pressure = data['current'].get('pressure', None)  # Handle missing 'pressure'
    if pressure is None:
        pressure = 0  # Default value for missing pressure

    # Extract and clean weather description
    weather_description = None
    if 'weather' in data['current'] and len(data['current']['weather']) > 0:
        weather_description = data['current']['weather'][0].get('description', None)
    if weather_description is None:
        weather_description = "No description available"  # Default value for missing description


    weather_data = {
        'temperature': temperature,  # Cleaned temperature
        'humidity': humidity,  # Cleaned humidity
        'pressure': pressure,  # Cleaned pressure
        'weather': weather_description  # Cleaned weather description
    }
    return weather_data

if __name__ == '__main__':
    api_key = 'afb285a23f1196fba343b39abddc9df0'
    lat = '41.8781'
    lon = '87.6298'
    weather_data = fetch_weather_data(api_key, lat, lon)
    df = pd.DataFrame([weather_data])
    df.to_csv('weather_data.csv', index=False)
    print(weather_data)  # Print the extracted weather data for debugging