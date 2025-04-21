import requests
import os
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta

def fetch_historical_weather_data(api_key, lat, lon, days=365):
    """Fetch historical weather data for the past year."""
    historical_data = []
    end_date = datetime.now()

    # Use tqdm for a progress bar
    for day in tqdm(range(days), desc="Fetching Historical Weather Data"):
        # Calculate the timestamp for each day
        timestamp = int((end_date - timedelta(days=day)).timestamp())
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}&units=imperial"
        
        response = requests.get(url)
        data = response.json()

        # Extract and clean daily data
        daily_data = {
            'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
            'temperature': round(data['data'][0]['temp'], 2) if 'data' in data and len(data['data']) > 0 else 0.0,
            'humidity': round(sum(hour.get('humidity', 0) for hour in data.get('data', [])) / len(data.get('data', [])), 2) if len(data.get('data', [])) > 0 else 0.0,  # Average humidity
            'precipitation': sum(hour.get('rain', {}).get('1h', 0) for hour in data.get('data', [])),  # Total precipitation
            'cloud_cover': sum(hour['clouds'] for hour in data.get('data', [])) / len(data.get('data', [])) if len(data.get('data', [])) > 0 else 0.0  # Average cloud cover
        }
        historical_data.append(daily_data)

    return pd.DataFrame(historical_data)

if __name__ == '__main__':
    # Load API key from environment variable
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the 'OPENWEATHER_API_KEY' environment variable.")

    lat = '41.8781'  # Chicago latitude
    lon = '-87.6298'  # Chicago longitude


    # # Fetch current weather data
    # current_weather = fetch_weather_data(api_key, lat, lon)
    # print("Current Weather Data:", current_weather)

    # # # Save current weather data to CSV
    # # current_df = pd.DataFrame([current_weather])
    # # current_df.to_csv('current_weather_data.csv', index=False)
    # # print("Current weather data saved to 'current_weather_data.csv'")

    # Fetch historical weather data
    historical_df = fetch_historical_weather_data(api_key, lat, lon, days=365)
    historical_df.to_csv('historical_weather_data.csv', index=False)
    print("Historical weather data saved to 'historical_weather_data.csv'")