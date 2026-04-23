#!/usr/bin/env python3
"""
Calendar Tools for Home Admin Agent
Includes tools for Google Calendar and Chronos MCP (CalDAV) integration.
"""

import os
import requests
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel, Field
from agent_models import BaseHomeTool, ToolMetadata

class GCalendarCreateArgs(BaseModel):
    summary: str = Field(..., description="The title or summary of the event.")
    description: Optional[str] = Field(None, description="The description of the event.")
    start_time: str = Field(..., description="Start time in ISO 8601 format (e.g., '2026-04-20T10:00:00Z').")
    end_time: str = Field(..., description="End time in ISO 8601 format.")
    location: Optional[str] = Field(None, description="Location of the event.")

class GCalendarCreateTool(BaseHomeTool):
    """Tool for creating events in Google Calendar."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="gcalendar_create_tool",
            description="Creates an event in Google Calendar.",
            args_schema=GCalendarCreateArgs,
            category="automation"
        )

    async def run(self, summary: str, start_time: str, end_time: str, description: Optional[str] = None, location: Optional[str] = None) -> str:
        access_token = os.getenv("GOOGLE_CALENDAR_ACCESS_TOKEN")
        if not access_token:
            return "Error: GOOGLE_CALENDAR_ACCESS_TOKEN not set."

        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        event_data = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time}
        }
        if location:
            event_data["location"] = location

        try:
            response = requests.post(url, headers=headers, json=event_data, timeout=10)
            response.raise_for_status()
            return f"Successfully created GCal event: {response.json().get('htmlLink')}"
        except Exception as e:
            return f"Error creating GCal event: {str(e)}"

class ChronosCalendarArgs(BaseModel):
    summary: str = Field(..., description="The title of the event.")
    description: Optional[str] = Field(None, description="The description of the event.")
    start_time: str = Field(..., description="Start time in ISO 8601 format.")
    end_time: str = Field(..., description="End time in ISO 8601 format.")
    calendar_url: str = Field(..., description="The CalDAV calendar URL.")

class ChronosCalendarTool(BaseHomeTool):
    """Tool for creating events via Chronos MCP (CalDAV)."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="chronos_calendar_tool",
            description="Creates an event in a CalDAV calendar (e.g., Proton, Nextcloud) via Chronos MCP logic.",
            args_schema=ChronosCalendarArgs,
            category="automation"
        )

    async def run(self, summary: str, start_time: str, end_time: str, calendar_url: str, description: Optional[str] = None) -> str:
        username = os.getenv("CALDAV_USERNAME")
        password = os.getenv("CALDAV_PASSWORD")

        if not username or not password:
            return "Error: CALDAV_USERNAME or CALDAV_PASSWORD not set."

        uid = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{summary.replace(' ', '-')[:20]}@homelab"

        def to_ical_time(iso_time):
            return iso_time.replace("-", "").replace(":", "").split(".")[0] + "Z"

        dtstart = to_ical_time(start_time)
        dtend = to_ical_time(end_time)
        dtstamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

        ical_payload = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Chronos MCP//Homelab//EN
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description or ''}
END:VEVENT
END:VCALENDAR"""

        event_url = f"{calendar_url.rstrip('/')}/{uid}.ics"
        headers = {"Content-Type": "text/calendar; charset=utf-8"}

        try:
            response = requests.put(
                event_url,
                data=ical_payload.encode('utf-8'),
                headers=headers,
                auth=(username, password),
                timeout=10
            )
            response.raise_for_status()
            return f"Successfully created CalDAV event at: {event_url}"
        except Exception as e:
            return f"Error creating CalDAV event: {str(e)}"

class CalendarEvent(BaseModel):
    summary: str
    start: str
    end: str

class ConflictCheckerArgs(BaseModel):
    start_time: str = Field(..., description="The start time to check (ISO 8601).")
    end_time: str = Field(..., description="The end time to check (ISO 8601).")
    existing_events: Optional[List[CalendarEvent]] = Field(None, description="List of existing events to check against.")
    calendar_ids: List[str] = Field(default=["primary"], description="List of calendar IDs to check.")

class ScheduleConflictCheckerTool(BaseHomeTool):
    """Tool for checking schedule conflicts."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="schedule_conflict_checker_tool",
            description="Checks for overlapping events. Can perform actual overlap logic if existing_events are provided.",
            args_schema=ConflictCheckerArgs,
            category="automation"
        )

    async def run(self, start_time: str, end_time: str, existing_events: Optional[List[CalendarEvent]] = None, calendar_ids: List[str] = ["primary"]) -> str:
        if not existing_events:
            # Mocking conflict check as full Free/Busy API integration requires complex setup
            # In a real scenario, this would call the GCal Free/Busy API
            return f"No conflicts found for the period {start_time} to {end_time} in calendars: {', '.join(calendar_ids)} (Simulated)."

        try:
            req_start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            req_end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except ValueError as e:
            return f"Error parsing requested times: {str(e)}"

        conflicts = []
        for event in existing_events:
            try:
                ev_start = datetime.fromisoformat(event.start.replace('Z', '+00:00'))
                ev_end = datetime.fromisoformat(event.end.replace('Z', '+00:00'))

                # Overlap logic: (StartA < EndB) and (EndA > StartB)
                if req_start < ev_end and req_end > ev_start:
                    conflicts.append(f"'{event.summary}' ({event.start} to {event.end})")
            except ValueError:
                continue

        if conflicts:
            return f"Conflict(s) detected: {', '.join(conflicts)}"
        else:
            return f"No conflicts found among {len(existing_events)} provided events for the period {start_time} to {end_time}."

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Calendar tools loaded.")
    asyncio.run(main())
