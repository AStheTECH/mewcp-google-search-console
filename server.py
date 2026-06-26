#!/usr/bin/env python3
"""MewCP Google Search Console MCP Server."""

import logging

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend
from starlette.responses import JSONResponse

from google_search_console_mcp.cli import parse_args
from google_search_console_mcp.config import BREAKING_CHANGES, SERVER_VERSION, configure_logging
from google_search_console_mcp.tools import register_tools

configure_logging()
logger = logging.getLogger("google-search-console-mcp")

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "MewCP Google Search Console MCP Server",
    version=SERVER_VERSION,
    middleware=[CredentialMiddleware(backend, "oauth")],
)
register_tools(mcp)


# /health MUST come before mcp.http_app() — routes are baked at http_app() time
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "service": mcp.name,
        "version": SERVER_VERSION,
        "breaking_changes": BREAKING_CHANGES,
    })


app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)


if __name__ == "__main__":
    args = parse_args()
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
    if args.host:
        run_kwargs["host"] = args.host
    if args.port:
        run_kwargs["port"] = args.port
    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server crashed: %s", e, exc_info=True)
        raise
