import os
from smolagents import OpenAIModel, CodeAgent, MCPClient, GradioUI, Tool

from .settings import OPENAI_API_KEY


class CarAgent:
    def __init__(self):
        self.model = OpenAIModel(
            model_id="gpt-4.1",
            api_key=OPENAI_API_KEY,
        )
        self.server_params = {
            "url": "http://127.0.0.1:8888/mcp/",
            "transport": "streamable-http"
        }
        self.mcp_client = MCPClient(server_parameters=self.server_params)
        self.tools: list[Tool] | None = None
        self.instructions = (
            "You are an assistant that helps users with their questions about cars. "
            "You can answer anything related to cars - but not anything else. "
            "If the user asks about anything other than cars, you should answer "
            "(in the same language as the question) that you can help them with cars, "
            "but you are not able to help them with anything else.\n"
            "If the user greets you, greet them by saying 'Hello! I'm CarBot. How can I help you with cars today?' "
            "- but adapt you answer to both the language and the tone the user is using.\n"
            "If the user asks you to search for a car, you should use the tools provided by the MCP server to find them. \n"
            "When listing the cars, you should always include: the make, model and year."
        )

    def run(self, prompt: str):
        if self.tools is None:
            raise Exception("Use a context manager in order to properly run the agent.")
        agent = CodeAgent(model=self.model, tools=self.tools, instructions=self.instructions)
        return agent.run(prompt)

    def run_webui(self):
        if self.tools is None:
            raise Exception("Use a context manager in order to properly run web interface.")
        agent = CodeAgent(model=self.model, tools=self.tools, instructions=self.instructions)
        GradioUI(agent).launch()

    def __enter__(self):
        self.tools = self.mcp_client.get_tools()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mcp_client.disconnect()
        return False
