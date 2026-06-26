"""Search group: get_search_analysis."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import SearchAnalysisData, SearchAnalysisRequest, SearchAnalysisResult
from ._helpers import _handle_sdk_exc

logger = logging.getLogger("google-search-console-mcp.tools.search")


def register_search_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_search_analysis",
        description=(
            "Query your search traffic data with filters and parameters that you define. "
            "The method returns zero or more rows grouped by the row keys (dimensions) that you define. "
            "You must define a date range of one or more days. When date is one of the dimensions, "
            "any days without data are omitted from the result list. To learn which days have data, "
            "issue a query without filters grouped by date, for the date range of interest. "
            "Results are sorted by click count descending. If two rows have the same click count, "
            "they are sorted in an arbitrary way."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_search_analysis(request: SearchAnalysisRequest) -> SearchAnalysisResult:
        tlog = ToolLogger(logger, "get_search_analysis")

        body = request.model_dump(exclude_none=True, exclude={"siteUrl"})

        try:
            svc = service.get_service()
            result = (
                svc.searchanalytics()
                .query(siteUrl=request.siteUrl, body=body)
                .execute()
            )
            tlog.success()
            return SearchAnalysisResult(
                success=True,
                statusCode=200,
                data=SearchAnalysisData(**result),
            )
        except Exception as exc:
            return _handle_sdk_exc(SearchAnalysisResult, tlog, exc)
