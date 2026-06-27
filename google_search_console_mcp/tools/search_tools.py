"""Search group: get_search_analysis."""

import logging
from typing import Literal

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import DimensionFilterGroup, SearchAnalysisData, SearchAnalysisResult
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
    def get_search_analysis(
        siteUrl: str = Field(
            ...,
            description="The site's URL, including protocol. For a URL-prefix property, supply the full URL (e.g. 'https://www.example.com/'). For a domain property, supply 'sc-domain:example.com'.",
        ),
        startDate: str = Field(
            ...,
            description="Start date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be less than or equal to the end date. This value is included in the range.",
        ),
        endDate: str = Field(
            ...,
            description="End date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be greater than or equal to the start date. This value is included in the range.",
        ),
        dimensions: list[str] | None = Field(
            None,
            description="Zero or more dimensions to group results by. Results are grouped in the order that you supply these dimensions. You can use any dimension name in dimensionFilterGroups[].filters[].dimension as well as date and hour. The grouping dimension values are combined to create a unique key for each result row. If no dimensions are specified, all values will be combined into a single row. There is no limit to the number of dimensions that you can group by, but you cannot group by the same dimension twice. Example: [country, device]",
        ),
        type: Literal["discover", "googleNews", "news", "image", "video", "web"] | None = Field(
            None,
            description="Filter results to the following type: discover: Discover results; googleNews: Results from news.google.com and the Google News app on Android and iOS. Doesn't include results from the News tab in Google Search., news: Search results from the News tab in Google Search., image: Search results from the Image tab in Google Search.; video: Video search results; web: [Default] Filter results to the combined (All) tab in Google Search. Does not include Discover or Google News results.",
        ),
        dimensionFilterGroups: list[DimensionFilterGroup] | None = Field(
            None,
            description="Zero or more groups of filters to apply to the dimension grouping values. All filter groups must match in order for a row to be returned in the response. Within a single filter group, you can specify whether all filters must match, or at least one must match.",
        ),
        aggregationType: Literal["auto", "byNewsShowcasePanel", "byPage", "byProperty"] | None = Field(
            None,
            description="How data is aggregated. 'auto': [Default] let the service decide. 'byNewsShowcasePanel': aggregate by News Showcase panel (requires the NEWS_SHOWCASE searchAppearance filter and type=discover or type=googleNews). 'byPage': aggregate by URI. 'byProperty': aggregate by property (not supported for type=discover or type=googleNews). Note: if you group or filter by page, you cannot aggregate by property.",
        ),
        rowLimit: int | None = Field(
            None,
            ge=1,
            le=25000,
            description="The maximum number of rows to return. Valid range is 1-25,000; default is 1,000. To page through results, use the startRow offset.",
        ),
        startRow: int | None = Field(
            None,
            ge=0,
            description="Zero-based index of the first row in the response. Must be a non-negative number. Default is 0. If startRow exceeds the number of results for the query, the response will be a successful response with zero rows.",
        ),
        dataState: Literal["all", "final", "hourly_all"] | None = Field(
            None,
            description="If 'all' (case-insensitive), data will include fresh data. If 'final' (case-insensitive) or if omitted, the returned data will include only finalized data. If 'hourly_all' (case-insensitive), data will include an hourly breakdown; this indicates that hourly data includes partial data and should be used when grouping by the HOUR API dimension.",
        ),
    ) -> SearchAnalysisResult:
        tlog = ToolLogger(logger, "get_search_analysis")

        body: dict = {"startDate": startDate, "endDate": endDate}
        if dimensions is not None:
            body["dimensions"] = dimensions
        if type is not None:
            body["type"] = type
        if dimensionFilterGroups is not None:
            body["dimensionFilterGroups"] = [g.model_dump(exclude_none=True) for g in dimensionFilterGroups]
        if aggregationType is not None:
            body["aggregationType"] = aggregationType
        if rowLimit is not None:
            body["rowLimit"] = rowLimit
        if startRow is not None:
            body["startRow"] = startRow
        if dataState is not None:
            body["dataState"] = dataState

        try:
            svc = service.get_service()
            result = (
                svc.searchanalytics()
                .query(siteUrl=siteUrl, body=body)
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
