import requests
import json

def test_weather_api():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.88,
        "longitude": -87.63,
        "current_weather": True
    }

    response = requests.get(url, params=params)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.json()
    assert "current_weather" in data, "Missing 'current_weather' in response"
    assert "temperature" in data["current_weather"], "Missing 'temperature' in current_weather"

    print("✅ Weather API test passed.")
    print("RESPONSE: " + json.dumps(data, indent=2))

if __name__ == "__main__":
    test_weather_api()
