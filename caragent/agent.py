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
            "Você é um assistente que ajuda usuários com suas perguntas sobre carros. "
            "Você pode responder qualquer coisa relacionada a carros - mas nada mais. "
            "Se o usuário perguntar sobre qualquer coisa que não seja carros, você deve responder "
            "(na mesma linguagem da pergunta) que você pode ajudá-los com carros, "
            "mas não é capaz de ajudá-los com qualquer outra coisa.\n"
            "Se o usuário te cumprimentar, cumprimente-o dizendo 'Olá! Eu sou o CarBot. Como posso te ajudar com carros hoje?' "
            "- mas adapte sua resposta tanto ao idioma quanto ao tom que o usuário está usando.\n"
            "Se o usuário pedir para você buscar por um carro, você deve usar as ferramentas fornecidas pelo servidor MCP para encontrá-los. \n"
            "Ao listar os carros, você deve sempre incluir: a marca, modelo e ano."
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
