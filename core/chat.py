from core.gemini import Gemini
from mcp_client import MCPClient
from core.tools import ToolManager
from google.genai import types


class Chat:
    def __init__(self, gemini_service: Gemini, clients: dict[str, MCPClient]):
        self.gemini_service: Gemini = gemini_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[types.Content] = []

    async def _process_query(self, query: str):
        self.gemini_service.add_user_message(self.messages, query)

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            response = self.gemini_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.gemini_service.add_model_message(self.messages, response)

            if self.gemini_service.has_tool_calls(response):
                text = self.gemini_service.text_from_message(response)
                if text:
                    print(text)
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.gemini_service.add_user_message(
                    self.messages, tool_result_parts
                )
            else:
                final_text_response = self.gemini_service.text_from_message(
                    response
                )
                break

        return final_text_response
