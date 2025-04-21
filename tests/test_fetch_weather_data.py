import unittest
from unittest.mock import patch
from src.fetch_weather_data import fetch_historical_weather_data

class TestFetchWeatherData(unittest.TestCase):
    @patch('fetch_historical_weather_data.requests.get')
    def test_fetch_weather_data(self, mock_get):
        # Mock API response
        mock_get.return_value.json.return_value = {
            "current": {
                "temp": 72.5,
                "humidity": 65,
                "pressure": 1013,
                "weather": [{"description": "clear sky"}]
            }
        }
        
        print("Mocked JSON Response:", mock_get.return_value.json.return_value)

        # Call the function
        api_key = "dummy_key"
        lat = "41.8781"
        lon = "-87.6298"
        result = fetch_historical_weather_data(api_key, lat, lon)

        print("Mock Called:", mock_get.called)

        # Assert the results
        self.assertEqual(result['temperature'], 72.5)
        self.assertEqual(result['humidity'], 65)
        self.assertEqual(result['pressure'], 1013)
        self.assertEqual(result['weather'], "clear sky")

if __name__ == '__main__':
    unittest.main()