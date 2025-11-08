# api-tests/test-sensors.py
import requests

response = requests.get("https://demo.smart-hub.io/api/sensors")
assert response.status_code == 200
assert "temperature" in response.json()
