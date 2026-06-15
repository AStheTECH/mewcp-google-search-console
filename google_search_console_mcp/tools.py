import logging
import json

from fastmcp import FastMCP

from .schemas import (
    ApiObjectResponse,
    SitemapRequestParams,
    SearchAnalysisRequest,
    ListSitemapRequestParams,
    SiteRequestParams,
    IndexInspectRequestBody
)
from google_search_console_mcp.service import get_service

logger = logging.getLogger("search-console-mcp-server")

class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)


@mcp.tool(
    name="get_search_analysis",
    description="Query your search traffic data with filters and parameters that you define. The method returns zero or more rows grouped by the row keys (dimensions) that you define. You must define a date range of one or more days. When date is one of the dimensions, any days without data are omitted from the result list. To learn which days have data, issue a query without filters grouped by date, for the date range of interest. Results are sorted by click count descending. If two rows have the same click count, they are sorted in an arbitrary way.",
)
def get_search_analysis(request: SearchAnalysisRequest) -> ApiObjectResponse:
    """Get Search Analysis"""
    logger.info(
        "Executing search analysis for %s (%s to %s)",
        request.siteUrl,
        request.startDate,
        request.endDate,
    )

    body = request.model_dump(exclude_none=True, exclude={"siteUrl"})

    try:
        service = get_service()
        result = (
            service.searchanalytics()
            .query(siteUrl=request.siteUrl, body=body)
            .execute()
        )
        return result
    except Exception as exc:
        logger.exception("Search analysis query failed")
        return {"error": str(exc)}


@mcp.tool(
    name="delete_sitemap",
    description="Deletes a sitemap from this site",
)
def delete_sitemap(params: SitemapRequestParams) -> ApiObjectResponse:
    """Delete a sitemap for this site"""
    logger.info(
        "deleting sitemap %s for %s",
        params.feedpath,
        params.siteUrl
    )


    try:
        service = get_service()
        result = (
            service.sitemaps()
            .delete(**params.model_dump(exclude_none=True))
            .execute()
        )
        return result or {"success": True, "message": "Sitemap deleted"}
    except Exception as exc:
        logger.exception("Delete sitemap query failed")
        return {"error": str(exc)}

@mcp.tool(
    name="get_sitemap",
    description="Retrieves information about a specific sitemap"
)
def get_sitemap(params: SitemapRequestParams) -> ApiObjectResponse:
    """Retrieves information about a specific sitemap"""
    logger.info(
        "getting sitemap %s for %s",
        params.feedpath,
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sitemaps().get(**params.model_dump(exclude_none=True)).execute()
        )

        return result

    except Exception as exc:
        logger.exception("Get sitemap query failed")
        return {"error": str(exc)}

@mcp.tool(
    name= "list_sitemap",
    description = "Lists the sitemaps-entries submitted for this site, or included in the sitemap index file (if sitemapIndex is specified in the request)."
)
def list_sitemap(params: ListSitemapRequestParams) -> ApiObjectResponse:
    """Lists the sitemaps-entries submitted for this site, or included in the sitemap index file (if sitemapIndex is specified in the request)."""
    logger.info(
        "getting sitemap for %s",
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sitemaps().list(**params.model_dump(exclude_none=True)).execute()
        )

        return result

    except Exception as exc:
        logger.exception("Get sitemap list query failed")
        return {"error": str(exc)}

@mcp.tool(
    name= "submit_sitemap",
    description = "Submits a sitemap for a site."
)
def submit_sitemap(params: SitemapRequestParams) -> ApiObjectResponse:
    """Submits a sitemap for a site."""
    logger.info(
        "submitting sitemap for %s",
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sitemaps().submit(**params.model_dump(exclude_none=True)).execute()
        )

        return result or {"success": True, "message": "Sitemap submitted"}

    except Exception as exc:
        logger.exception("submit sitemap query failed")
        return {"error": str(exc)}


@mcp.tool(
    name= "add_site",
    description = "Adds a site to the set of the user's sites in Search Console."
)
def add_site(params: SiteRequestParams) -> ApiObjectResponse:
    """Adds a site to the set of the user's sites in Search Console."""
    logger.info(
        "adding site %s to search console",
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sites().add(**params.model_dump(exclude_none=True)).execute()
        )

        return result or {"success": True, "message": "Site added"}

    except Exception as exc:
        logger.exception("add site query failed")
        return {"error": str(exc)}

@mcp.tool(
    name= "delete_site",
    description = "Removes a site from the set of the user's Search Console sites."
)
def delete_site(params: SiteRequestParams) -> ApiObjectResponse:
    """Removes a site from the set of the user's Search Console sites."""
    logger.info(
        "deleting site %s",
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sites().delete(**params.model_dump(exclude_none=True)).execute()
        )

        return result or {"success": True, "message": "Site deleted"}

    except Exception as exc:
        logger.exception("delete site query failed")
        return {"error": str(exc)}

@mcp.tool(
    name= "get_site",
    description = "Retrieves information about specific site."
)
def get_site(params: SiteRequestParams) -> ApiObjectResponse:
    """Retrieves information about specific site. """
    logger.info(
        "retrieving site %s",
        params.siteUrl
    )

    try:
        service = get_service()
        result = (
            service.sites().get(**params.model_dump(exclude_none=True)).execute()
        )

        return result

    except Exception as exc:
        logger.exception("get site query failed")
        return {"error": str(exc)}


@mcp.tool(
    name= "list_sites",
    description = "Lists the user's Search Console sites."
)
def list_sites() -> ApiObjectResponse:
    """Lists the user's Search Console sites."""
    logger.info("retrieving list of site on search console")

    try:
        service = get_service()
        result =  service.sites().list().execute()
        return result

    except Exception as exc:
        logger.exception("list sites query failed")
        return {"error": str(exc)}

@mcp.tool(
    name= "inspect_index",
    description = "View the indexed, or indexable, status of the provided URL. Presently only the status of the version in the Google index is available; you cannot test the indexability of a live URL."
)
def index_inspect(body: IndexInspectRequestBody) -> ApiObjectResponse:
    """View the indexed, or indexable, status of the provided URL. Presently only the status of the version in the Google index is available; you cannot test the indexability of a live URL."""
    logger.info("inspecting the indexability of %s", body.inspectionUrl)

    try:
        service = get_service()
        result = (
            service.urlInspection()
            .index()
            .inspect(body=body.model_dump(exclude_none=True))
            .execute()
        )
        return result

    except Exception as exc:
        logger.exception("inspection of url failed")
        return {"error": str(exc)}

@mcp.tool(
    name="google_search_console_health_check",
    description="Check server readiness and basic connectivity.",
)
def google_search_console_health_check() -> str:
    """Health check endpoint."""
    return json.dumps(
        {
            "status": "ok",
            "server": "Google Search Console API MCP Server",
            "type": "third-party integration",
            "auth_required": "oauth token required",
        }
    )
