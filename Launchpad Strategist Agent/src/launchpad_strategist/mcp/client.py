import asyncio
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, Optional

import mcp
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


def run_async(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(lambda: asyncio.run(coro)).result()


class LaunchpadMCPClient:
    def __init__(self) -> None:
        server_path = str((Path(__file__).resolve().parents[3] / "server.py").resolve())
        self.params = StdioServerParameters(command=sys.executable, args=[server_path], env=os.environ.copy())

    @staticmethod
    def _tool_result_to_text(result: Any) -> str:
        if hasattr(result, "content") and result.content:
            chunk = result.content[0]
            if hasattr(chunk, "text"):
                return chunk.text
        return str(result)

    @staticmethod
    def _resource_result_to_text(result: Any) -> str:
        if hasattr(result, "contents") and result.contents:
            chunk = result.contents[0]
            if hasattr(chunk, "text"):
                return chunk.text
        return str(result)

    async def call_tool_async(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        async with stdio_client(self.params) as streams:
            async with mcp.ClientSession(*streams) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments or {})
                return self._tool_result_to_text(result)

    async def read_resource_async(self, uri: str) -> str:
        async with stdio_client(self.params) as streams:
            async with mcp.ClientSession(*streams) as session:
                await session.initialize()
                result = await session.read_resource(uri)
                return self._resource_result_to_text(result)

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        return run_async(self.call_tool_async(name, arguments))

    def read_resource(self, uri: str) -> str:
        return run_async(self.read_resource_async(uri))
