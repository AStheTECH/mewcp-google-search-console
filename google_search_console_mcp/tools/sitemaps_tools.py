"""Sitemaps group: delete_sitemap, get_sitemap, list_sitemap, submit_sitemap"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    DeleteSitemapData,
    DeleteSitemapResult,
    ListSitemapRequestParams,
    SitemapData,
    SitemapListData,
    SitemapListResult,
    SitemapRequestParams,
    SitemapResult,
    SubmitSitemapData,
    SubmitSitemapResult,
)
from ._helpers import _handle_sdk_exc

logger = logging.getLogger("google-search-console-mcp.tools.sitemaps")


def register_sitemaps_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="delete_sitemap",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes a sitemap from this site. "
            "This action is irreversible — the sitemap entry cannot be recovered once deleted. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=True, openWorldHint=True
        ),
    )
    def delete_sitemap(params: SitemapRequestParams) -> DeleteSitemapResult:
        tlog = ToolLogger(logger, "delete_sitemap")

        try:
            svc = service.get_service()
            result = svc.sitemaps().delete(**params.model_dump(exclude_none=True)).execute()
            data = result or {"success": True, "message": "Sitemap deleted"}
            tlog.success()
            return DeleteSitemapResult(success=True, statusCode=200, data=DeleteSitemapData(**data))
        except Exception as exc:
            return _handle_sdk_exc(DeleteSitemapResult, tlog, exc)

    @mcp.tool(
        name="get_sitemap",
        description=(
            "Retrieves information about a specific sitemap."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def get_sitemap(params: SitemapRequestParams) -> SitemapResult:
        tlog = ToolLogger(logger, "get_sitemap")

        try:
            svc = service.get_service()
            result = svc.sitemaps().get(**params.model_dump(exclude_none=True)).execute()
            tlog.success()
            return SitemapResult(success=True, statusCode=200, data=SitemapData(**result))
        except Exception as exc:
            return _handle_sdk_exc(SitemapResult, tlog, exc)

    @mcp.tool(
        name="list_sitemap",
        description=(
            "Lists the sitemaps-entries submitted for this site, or included in the sitemap index "
            "file (if sitemapIndex is specified in the request)."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def list_sitemap(params: ListSitemapRequestParams) -> SitemapListResult:
        tlog = ToolLogger(logger, "list_sitemap")

        try:
            svc = service.get_service()
            result = svc.sitemaps().list(**params.model_dump(exclude_none=True)).execute()
            tlog.success()
            return SitemapListResult(success=True, statusCode=200, data=SitemapListData(**result))
        except Exception as exc:
            return _handle_sdk_exc(SitemapListResult, tlog, exc)

    @mcp.tool(
        name="submit_sitemap",
        description=(
            "Submits a sitemap for a site."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, openWorldHint=True
        ),
    )
    def submit_sitemap(params: SitemapRequestParams) -> SubmitSitemapResult:
        tlog = ToolLogger(logger, "submit_sitemap")

        try:
            svc = service.get_service()
            result = svc.sitemaps().submit(**params.model_dump(exclude_none=True)).execute()
            data = result or {"success": True, "message": "Sitemap submitted"}
            tlog.success()
            return SubmitSitemapResult(success=True, statusCode=200, data=SubmitSitemapData(**data))
        except Exception as exc:
            return _handle_sdk_exc(SubmitSitemapResult, tlog, exc)
