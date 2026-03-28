from mcp.server.fastmcp import FastMCP


mcp = FastMCP("launchpad_strategist_server")


def create_server() -> FastMCP:
    from launchpad_strategist.mcp import resources  # noqa: F401
    from launchpad_strategist.mcp.tools import analysis  # noqa: F401
    from launchpad_strategist.mcp.tools import sessions  # noqa: F401

    return mcp


def run_server() -> None:
    create_server().run(transport="stdio")
