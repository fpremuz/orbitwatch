from app.ai.tools.alert_tools import AlertStatsTool
from app.ai.tools.alert_tools import LatestAlertTool
from app.ai.tools.satellite_tools import SatelliteCountTool
from app.ai.tools.satellite_tools import SatelliteListTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "satellite_count": SatelliteCountTool(),
            "satellite_list": SatelliteListTool(),
            "latest_alert": LatestAlertTool(),
            "alert_stats": AlertStatsTool(),
        }

    def execute(self, tool_name: str) -> str:

        tool = self.tools.get(tool_name)

        if tool is None:
            return "Unknown tool."

        return tool.execute()