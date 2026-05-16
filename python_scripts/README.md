# Location History Tracking

This custom solution provides historic location-based weather tracking using Python scripts and the OpenWeatherMap API.

## How It Works

1. **Location Change Detection** - An automation triggers whenever a person's location changes
2. **GPS Recording** - The Python script records GPS coordinates, timestamp, and zone
3. **Weather Fetching** - For each location, it fetches current weather from OpenWeatherMap API
4. **History Storage** - Data is stored in an `input_text` entity as JSON
5. **Daily Recap** - The main blueprint reads the history and feeds it to the LLM

## Setup Instructions

### Step 1: Enable Python Scripts

Add to your `configuration.yaml`:
```yaml
python_script:
```

### Step 2: Create Helper Entities

Create `input_text` entities for each person you want to track:

**Via Settings > Devices & Services > Helpers:**
1. Create Text helper: `location_history_roald` (max 255 chars)
2. Create Text helper: `location_summary_roald` (max 255 chars)
3. Repeat for other people

Or add to `configuration.yaml`:
```yaml
input_text:
  location_history_roald:
    name: "Location History - Roald"
    initial: "[]"
    max: 255
  location_summary_roald:
    name: "Location Summary - Roald"
    initial: "No location data"
    max: 255
```

### Step 3: Copy Python Scripts

Copy these files to your Home Assistant `python_scripts` folder:
- `track_location_history.py`
- `generate_location_recap.py`

### Step 4: Get OpenWeatherMap API Key

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Add to `secrets.yaml`:
```yaml
openweathermap_api_key: "your-api-key-here"
```

### Step 5: Create Location Tracking Automation

Create an automation for each person:

```yaml
alias: "Track Location History - Roald"
trigger:
  - platform: state
    entity_id: person.roald
    not_to:
      - "unavailable"
      - "unknown"
action:
  - service: python_script.track_location_history
    data:
      device_tracker: "person.roald"
      history_entity: "input_text.location_history_roald"
      summary_entity: "input_text.location_summary_roald"
      person_name: "Roald"
      owm_api_key: "!secret openweathermap_api_key"
```

### Step 6: Configure Daily Recap Blueprint

When importing the daily recap blueprint:
1. Add the location history entities to **"Location History Summaries"**
2. Select your `input_text.location_summary_*` entities

## Data Structure

Each location entry contains:
```json
{
  "timestamp": "2024-05-16T14:30:00",
  "location": "zone.work",
  "latitude": 51.1234,
  "longitude": 4.5678,
  "gps_accuracy": 20,
  "person": "Roald",
  "weather": {
    "condition": "few clouds",
    "temperature": 22.5,
    "feels_like": 23.1,
    "humidity": 65,
    "wind_speed": 3.2,
    "location_name": "Antwerp"
  }
}
```

## Limitations

- `input_text` has a 255 character limit, so history is limited (~10-15 entries)
- Weather is fetched at the time of location change, not historical weather
- Requires OpenWeatherMap API (free tier: 60 calls/minute, 1,000,000 calls/month)

## Troubleshooting

### Check service is registered
Go to Developer Tools > Services and search for "python_script" - you should see your scripts listed.

### Check history is being recorded
Go to Developer Tools > States and look for your `input_text.location_history_*` entities.

### View logs
Add to your automation to debug:
```yaml
- service: system_log.write
  data:
    level: info
    message: "Location tracked for {{ trigger.to_state.attributes.friendly_name }}"
```
