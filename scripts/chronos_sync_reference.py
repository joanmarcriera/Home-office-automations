import os
import requests
from datetime import datetime, timedelta, timezone

# Reference implementation for Chronos MCP / CalDAV Event Creation
# This script demonstrates how to create an event via a CalDAV-compliant server.
# In the context of Chronos MCP, this would be the interaction between the MCP server and the calendar provider.

def create_caldav_event(summary, description, start_time_iso, end_time_iso, calendar_url):
    """
    Creates an event in a CalDAV calendar using a PUT request with an iCalendar payload.
    Requires CalDAV URL and authentication (usually Basic Auth).
    """
    username = os.getenv("CALDAV_USERNAME")
    password = os.getenv("CALDAV_PASSWORD")

    if not username or not password:
        print("Error: CALDAV_USERNAME or CALDAV_PASSWORD not found in environment.")
        return None

    # Generate a unique UID for the event
    uid = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{summary.replace(' ', '-')[:20]}@homelab"

    # Format times for iCalendar (YYYYMMDDTHHMMSSZ)
    def to_ical_time(iso_time):
        return iso_time.replace("-", "").replace(":", "").split(".")[0] + "Z"

    dtstart = to_ical_time(start_time_iso)
    dtend = to_ical_time(end_time_iso)
    dtstamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

    # Minimal iCalendar payload
    ical_payload = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Chronos MCP//Homelab//EN
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR"""

    # Target URL for the new resource
    event_url = f"{calendar_url.rstrip('/')}/{uid}.ics"

    headers = {
        "Content-Type": "text/calendar; charset=utf-8"
    }

    try:
        response = requests.put(
            event_url,
            data=ical_payload.encode('utf-8'),
            headers=headers,
            auth=(username, password)
        )
        response.raise_for_status()
        print(f"Event created successfully: {event_url}")
        return {"uid": uid, "url": event_url}
    except Exception as e:
        print(f"Failed to create CalDAV event: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Details: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    test_summary = "Proton Calendar Task"
    test_desc = "Automated reminder from Chronos MCP integration"
    test_calendar_url = "https://your-caldav-server.com/remote.php/dav/calendars/user/personal/"

    test_start = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    test_end = (datetime.now(timezone.utc) + timedelta(days=2, hours=1)).isoformat()

    print("Testing CalDAV Event Creation (Dry Run / No Auth)...")
    # In a real run, you'd provide valid environment variables and URL
    # create_caldav_event(test_summary, test_desc, test_start, test_end, test_calendar_url)
