import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "basic_agent.mcp_server"],
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)
            result = await session.call_tool(
                "privacy_guard",
                {"text": "Contact me at student@gmail.com"},
            )
            print("\nPrivacy Guard result:")
            print(result.content)

            result = await session.call_tool(
                "sampling_analyzer",
                {
                    "probabilities": [0.7, 0.2, 0.1],
                    "temperature": 2.0,
                },
            )
            print("\nSampling Analyzer result:")
            print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
