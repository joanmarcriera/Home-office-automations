import unittest
from unittest.mock import patch, MagicMock
import asyncio
import os

# Set dummy environment variables for tools
os.environ["VIKUNJA_API_TOKEN"] = "fake_vikunja_token"
os.environ["HOME_ASSISTANT_TOKEN"] = "fake_ha_token"

from vikunja_tool import VikunjaCreateTool, VikunjaUpdateTool, VikunjaRelationTool
from home_assistant_tool import HAStateQueryTool, HASceneTriggerTool, HALightControlTool

class TestHomeAdminTools(unittest.IsolatedAsyncioTestCase):

    @patch('requests.put')
    async def test_vikunja_create_tool(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 123, "title": "Test Task"}
        mock_put.return_value = mock_response

        tool = VikunjaCreateTool()
        result = await tool.run(title="Test Task", project_id=1)

        self.assertIn("Successfully created task 'Test Task' with ID: 123", result)
        mock_put.assert_called_once()

    @patch('requests.post')
    async def test_vikunja_update_tool(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        tool = VikunjaUpdateTool()
        result = await tool.run(task_id=123, title="Updated Task")

        self.assertIn("Successfully updated task ID: 123", result)
        mock_post.assert_called_once()

    @patch('requests.get')
    async def test_ha_state_query_tool(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "state": "on",
            "attributes": {"friendly_name": "Living Room Light"}
        }
        mock_get.return_value = mock_response

        tool = HAStateQueryTool()
        result = await tool.run(entity_id="light.living_room")

        self.assertIn("Entity 'Living Room Light' (light.living_room) is currently 'on'", result)
        mock_get.assert_called_once()

    @patch('requests.post')
    async def test_ha_light_control_tool(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        tool = HALightControlTool()
        result = await tool.run(entity_id="light.living_room", action="turn_on", brightness=200)

        self.assertIn("Successfully performed 'turn_on' on light 'light.living_room'", result)
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()
