"""Sites group: add_site, delete_site, get_site, list_sites."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    AddSiteData,
    AddSiteResult,
    DeleteSiteData,
    DeleteSiteResult,
    SiteData,
    SiteListData,
    SiteListResult,
    SiteResult,
)
from ._helpers import _handle_sdk_exc

logger = logging.getLogger("google-search-console-mcp.tools.sites")


def register_sites_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="add_site",
        description="Adds a site to the set of the user's sites in Search Console.",
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, openWorldHint=True
        ),
    )
    def add_site(
        siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/"),
    ) -> AddSiteResult:
        tlog = ToolLogger(logger, "add_site")

        try:
            svc = service.get_service()
            result = svc.sites().add(siteUrl=siteUrl).execute()
            tlog.success()
            return AddSiteResult(
                success=True,
                statusCode=200,
                data=AddSiteData(**(result or {"success": True, "message": "Site added"})),
            )
        except Exception as exc:
            return _handle_sdk_exc(AddSiteResult, tlog, exc)

    @mcp.tool(
        name="delete_site",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently removes a site from the set of the user's Search Console sites. "
            "This action is irreversible — the site entry cannot be recovered once deleted. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=True, openWorldHint=True
        ),
    )
    def delete_site(
        siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/"),
    ) -> DeleteSiteResult:
        tlog = ToolLogger(logger, "delete_site")

        try:
            svc = service.get_service()
            result = svc.sites().delete(siteUrl=siteUrl).execute()
            tlog.success()
            return DeleteSiteResult(
                success=True,
                statusCode=200,
                data=DeleteSiteData(
                    **(result or {"success": True, "message": "Site deleted"})
                ),
            )
        except Exception as exc:
            return _handle_sdk_exc(DeleteSiteResult, tlog, exc)

    @mcp.tool(
        name="get_site",
        description="Retrieves information about specific site.",
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def get_site(
        siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/"),
    ) -> SiteResult:
        tlog = ToolLogger(logger, "get_site")

        try:
            svc = service.get_service()
            result = svc.sites().get(siteUrl=siteUrl).execute()
            tlog.success()
            return SiteResult(success=True, statusCode=200, data=SiteData(**result))
        except Exception as exc:
            return _handle_sdk_exc(SiteResult, tlog, exc)

    @mcp.tool(
        name="list_sites",
        description="Lists the user's Search Console sites.",
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def list_sites() -> SiteListResult:
        tlog = ToolLogger(logger, "list_sites")

        try:
            svc = service.get_service()
            result = svc.sites().list().execute()
            tlog.success()
            return SiteListResult(
                success=True, statusCode=200, data=SiteListData(**result)
            )
        except Exception as exc:
            return _handle_sdk_exc(SiteListResult, tlog, exc)
