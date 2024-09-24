from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)

OPENWEATHER_API_KEY = '4df0d76850d8b55311fb5c1fc3a90e2c'
OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Sample data
mock_data = {
    "alerts": [
        "Poaching incident reported in Kruger National Park.",
        "Illegal logging detected in Limpopo province.",
    ],
    "locations": [
        {"province": "Mpumalanga", "latitude": -25.3463, "longitude": 31.0260, "incidents": 5},
        {"province": "Limpopo", "latitude": -23.8962, "longitude": 29.4593, "incidents": 2},
    ],
    "trends": [
        {"date": "2024-01-01", "count": random.randint(1, 10)},
        {"date": "2024-02-01", "count": random.randint(1, 10)},
    ]
}

def get_weather_data(latitude, longitude):
    """Fetch weather data from OpenWeatherMap API."""
    response = requests.get(OPENWEATHER_API_URL, params={
        'lat': latitude,
        'lon': longitude,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    })
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    for location in mock_data['locations']:
        weather_data = get_weather_data(location['latitude'], location['longitude'])
        location['weather'] = weather_data.get('weather', [{}])[0].get('description', 'No data')
        location['temperature'] = weather_data.get('main', {}).get('temp', 'N/A')

    return jsonify(mock_data)

if __name__ == '__main__':
    app.run(debug=True)
