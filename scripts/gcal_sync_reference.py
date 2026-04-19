import os
import requests
from datetime import datetime, timedelta

# Reference implementation for Google Calendar Event Creation
# This script would typically be called by an n8n workflow or a backend service.

def create_gcal_event(summary, description, start_time_iso, end_time_iso, location=None):
    """
    Creates an event in Google Calendar using the REST API.
    Requires a valid OAuth2 Access Token.
    """
    # In a real scenario, this token would be managed by n8n or an OAuth proxy
    access_token = os.getenv("GOOGLE_CALENDAR_ACCESS_TOKEN")

    if not access_token:
        print("Error: GOOGLE_CALENDAR_ACCESS_TOKEN not found in environment.")
        return None

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    event_data = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time_iso,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time_iso,
            "timeZone": "UTC"
        }
    }

    if location:
        event_data["location"] = location

    try:
        response = requests.post(url, headers=headers, json=event_data)
        response.raise_for_status()
        print(f"Event created successfully: {response.json().get('htmlLink')}")
        return response.json()
    except Exception as e:
        print(f"Failed to create event: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Details: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    test_summary = "Water Bill Due"
    test_desc = "Automated reminder from Home Admin Agent"
    test_start = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
    test_end = (datetime.utcnow() + timedelta(days=7, hours=1)).isoformat() + "Z"

    print("Testing GCal Event Creation (Dry Run / No Token)...")
    create_gcal_event(test_summary, test_desc, test_start, test_end)
