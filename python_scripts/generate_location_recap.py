"""
Generate a recap from location history for the LLM.
This script processes stored location history and formats it for the daily recap.

Usage in automation:
  service: python_script.generate_location_recap
  data:
    history_entity: input_text.location_history_roald
"""

import json
from datetime import datetime

# Get parameters
history_entity = data.get("history_entity", "")
summary_entity = data.get("summary_entity", "")

if not history_entity:
    logger.error("generate_location_recap: No history_entity specified")
    exit()

if not summary_entity:
    logger.error("generate_location_recap: No summary_entity specified")
    exit()

# Get location history
history_state = hass.states.get(history_entity)
if not history_state:
    logger.warning(f"History entity {history_entity} not found")
    hass.services.call("input_text", "set_value", {
        "entity_id": summary_entity,
        "value": "No location history available"
    })
    exit()

try:
    history = json.loads(history_state.state)
    if not isinstance(history, list) or len(history) == 0:
        raise ValueError("Empty or invalid history")
except Exception as e:
    logger.error(f"Error parsing history: {e}")
    hass.services.call("input_text", "set_value", {
        "entity_id": summary_entity,
        "value": "No location history available"
    })
    exit()

# Get today's entries
today = datetime.now().date()
today_entries = [
    entry for entry in history
    if datetime.fromisoformat(entry.get("timestamp", "")).date() == today
]

if not today_entries:
    logger.info("No location entries for today")
    hass.services.call("input_text", "set_value", {
        "entity_id": summary_entity,
        "value": "No location history for today"
    })
    exit()

# Group by location visited
locations_visited = {}
for entry in today_entries:
    loc = entry.get("location", "unknown")
    if loc not in locations_visited:
        locations_visited[loc] = {
            "first_seen": entry.get("timestamp"),
            "last_seen": entry.get("timestamp"),
            "count": 0,
            "weather_samples": []
        }
    locations_visited[loc]["count"] += 1
    locations_visited[loc]["last_seen"] = entry.get("timestamp")

    if "weather" in entry:
        locations_visited[loc]["weather_samples"].append(entry["weather"])

# Build summary
summary_parts = []
person_name = today_entries[0].get("person", "You")

for location, data in locations_visited.items():
    first_time = datetime.fromisoformat(data["first_seen"]).strftime("%H:%M")
    last_time = datetime.fromisoformat(data["last_seen"]).strftime("%H:%M")

    # Get most common weather or latest weather
    weather_desc = ""
    if data["weather_samples"]:
        # Use the most recent weather
        latest_weather = data["weather_samples"][-1]
        temp = latest_weather.get("temperature", "unknown")
        condition = latest_weather.get("condition", "unknown")
        location_name = latest_weather.get("location_name", location)
        weather_desc = f" - Weather: {condition}, {temp}°C in {location_name}"

    location_display = location
    if location == "home":
        location_display = "at home"
    elif location == "not_home":
        location_display = "away from home"
    else:
        location_display = f"at {location}"

    summary_parts.append(
        f"{person_name} was {location_display} "
        f"from {first_time} to {last_time}{weather_desc}"
    )

# Combine into final summary
final_summary = "\n".join(summary_parts)

# Save to summary entity
hass.services.call("input_text", "set_value", {
    "entity_id": summary_entity,
    "value": final_summary
})

logger.info(f"Location recap generated for {person_name}: {len(today_entries)} entries")
