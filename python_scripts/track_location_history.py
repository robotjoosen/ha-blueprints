"""
Track device location history and fetch weather data.
This script should be called when a device location changes.

Configuration in automations.yaml:
- Requires OpenWeatherMap API key
- Requires input_text entity to store history
"""

# Get parameters from service call
device_tracker = data.get("device_tracker", "")
history_entity = data.get("history_entity", "")
own_name = data.get("person_name", "Someone")
owm_api_key = data.get("owm_api_key", "")

if not device_tracker:
    logger.error("track_location_history: No device_tracker specified")
    hass.services.call("persistent_notification", "create", {
        "title": "Location History Error",
        "message": "Device tracker not specified"
    })
    exit()

if not history_entity:
    logger.error("track_location_history: No history_entity specified")
    hass.services.call("persistent_notification", "create", {
        "title": "Location History Error",
        "message": "History entity not specified"
    })
    exit()

# Get current location data
state = hass.states.get(device_tracker)
if not state:
    logger.error(f"track_location_history: Device tracker {device_tracker} not found")
    exit()

location = state.state
lat = state.attributes.get("latitude")
lon = state.attributes.get("longitude")
gps_accuracy = state.attributes.get("gps_accuracy", "unknown")

# Get existing history
history_state = hass.states.get(history_entity)
if history_state:
    try:
        import json
        history = json.loads(history_state.state)
        if not isinstance(history, list):
            history = []
    except:
        history = []
else:
    history = []

# Get current timestamp
from datetime import datetime
timestamp = datetime.now().isoformat()

# Create location entry
location_entry = {
    "timestamp": timestamp,
    "location": location,
    "latitude": lat,
    "longitude": lon,
    "gps_accuracy": gps_accuracy,
    "person": person_name
}

# Fetch weather if we have coordinates and OWM API key
if lat and lon and owm_api_key:
    try:
        import requests
        # OpenWeatherMap Current Weather API
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={owm_api_key}&units=metric"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            weather_data = response.json()
            location_entry["weather"] = {
                "condition": weather_data["weather"][0]["description"],
                "temperature": weather_data["main"]["temp"],
                "feels_like": weather_data["main"]["feels_like"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
                "location_name": weather_data["name"]
            }
        else:
            logger.warning(f"OWM API returned status {response.status_code}")
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")

# Add to history (keep last 50 entries)
history.append(location_entry)
if len(history) > 50:
    history = history[-50:]

# Save history
import json
hass.services.call("input_text", "set_value", {
    "entity_id": history_entity,
    "value": json.dumps(history)
})

logger.info(f"Location history updated for {person_name}: {location}")
