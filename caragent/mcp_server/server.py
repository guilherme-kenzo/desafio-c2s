from mcp.server.fastmcp import FastMCP
from ..settings import MCP_HOST, MCP_PORT


mcp = FastMCP(
    name="car-mcp-server",
    version="1.0.0",
    host=MCP_HOST,
    port=MCP_PORT
)


