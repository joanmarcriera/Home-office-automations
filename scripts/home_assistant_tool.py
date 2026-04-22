#!/usr/bin/env python3
"""
Home Assistant Tools for Home Admin Agent
Allows the agent to query entity states, trigger scenes, and control lights in Home Assistant via its REST API.
"""

import os
import requests
from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel, Field
from agent_models import BaseHomeTool, ToolMetadata

class HAStateQueryArgs(BaseModel):
    entity_id: str = Field(..., description="The entity ID to query (e.g., 'light.living_room').")

class HAStateQueryTool(BaseHomeTool):
    """Tool for querying the state of an entity in Home Assistant."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="ha_state_query_tool",
            description="Queries the current state and attributes of a specified Home Assistant entity.",
            args_schema=HAStateQueryArgs,
            category="automation"
        )

    async def run(self, entity_id: str) -> str:
        api_url = os.environ.get("HOME_ASSISTANT_URL", "http://localhost:8123/api")
        api_token = os.environ.get("HOME_ASSISTANT_TOKEN")

        if not api_token:
            return "Error: HOME_ASSISTANT_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        try:
            endpoint = f"{api_url}/states/{entity_id}"
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()

            state_data = response.json()
            state = state_data.get("state")
            attributes = state_data.get("attributes", {})
            friendly_name = attributes.get("friendly_name", entity_id)

            return f"Entity '{friendly_name}' ({entity_id}) is currently '{state}'."

        except requests.exceptions.RequestException as e:
            return f"Error querying Home Assistant: {str(e)}"

class HASceneTriggerArgs(BaseModel):
    scene_id: str = Field(..., description="The entity ID of the scene to trigger (e.g., 'scene.movie_night').")

class HASceneTriggerTool(BaseHomeTool):
    """Tool for triggering a scene in Home Assistant."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="ha_scene_trigger_tool",
            description="Triggers a specified scene in Home Assistant.",
            args_schema=HASceneTriggerArgs,
            category="automation"
        )

    async def run(self, scene_id: str) -> str:
        api_url = os.environ.get("HOME_ASSISTANT_URL", "http://localhost:8123/api")
        api_token = os.environ.get("HOME_ASSISTANT_TOKEN")

        if not api_token:
            return "Error: HOME_ASSISTANT_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        data = {"entity_id": scene_id}

        try:
            endpoint = f"{api_url}/services/scene/turn_on"
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            response.raise_for_status()

            return f"Successfully triggered scene '{scene_id}'."

        except requests.exceptions.RequestException as e:
            return f"Error triggering Home Assistant scene: {str(e)}"

class HALightControlArgs(BaseModel):
    entity_id: str = Field(..., description="The entity ID of the light to control.")
    action: str = Field(..., description="Action to perform: 'turn_on' or 'turn_off'.")
    brightness: Optional[int] = Field(None, description="Brightness level (0-255) if action is 'turn_on'.")

class HALightControlTool(BaseHomeTool):
    """Tool for controlling lights in Home Assistant."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="ha_light_control_tool",
            description="Controls a light in Home Assistant (turn on/off, adjust brightness).",
            args_schema=HALightControlArgs,
            category="automation"
        )

    async def run(self, entity_id: str, action: str, brightness: Optional[int] = None) -> str:
        api_url = os.environ.get("HOME_ASSISTANT_URL", "http://localhost:8123/api")
        api_token = os.environ.get("HOME_ASSISTANT_TOKEN")

        if not api_token:
            return "Error: HOME_ASSISTANT_TOKEN not set in environment."

        if action not in ["turn_on", "turn_off"]:
            return "Error: action must be 'turn_on' or 'turn_off'."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        data = {"entity_id": entity_id}
        if action == "turn_on" and brightness is not None:
            data["brightness"] = brightness

        try:
            endpoint = f"{api_url}/services/light/{action}"
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            response.raise_for_status()

            return f"Successfully performed '{action}' on light '{entity_id}'."

        except requests.exceptions.RequestException as e:
            return f"Error controlling Home Assistant light: {str(e)}"

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Home Assistant tools loaded.")
    asyncio.run(main())
