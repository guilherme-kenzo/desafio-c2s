from dotenv import load_dotenv
import os

load_dotenv(".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "sqlite:///cars.db")
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", 8888))