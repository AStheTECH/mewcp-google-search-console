"""MewCP Google Search Console tool registration."""

from fastmcp import FastMCP

from .search_tools import register_search_tools
from .sitemaps_tools import register_sitemaps_tools
from .sites_tools import register_sites_tools
from .url_inspection_tools import register_url_inspection_tools


def register_tools(mcp: FastMCP) -> None:
    register_search_tools(mcp)
    register_sitemaps_tools(mcp)
    register_sites_tools(mcp)
    register_url_inspection_tools(mcp)
