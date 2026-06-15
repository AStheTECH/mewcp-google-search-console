from typing import Any, Optional, TypedDict, Literal, List
from pydantic import BaseModel, Field


class ToolError(TypedDict):
    error: str


SearchToolResponse = dict[str, Any] | ToolError

ApiObjectResponse = dict[str, Any] | ToolError


class DimensionFilter(BaseModel):
    """A single filter to test against a row: a dimension, an operator, and a value."""

    dimension: Literal["country", "device", "page", "query", "searchAppearance"] = Field(
        ...,
        description="The dimension that this filter applies to. You can filter by any dimension even if you are not grouping by it. 'country': 3-letter country code (ISO 3166-1 alpha-3). 'device': DESKTOP, MOBILE or TABLET. 'page': a URI string. 'query': a query string. 'searchAppearance': a specific search result feature.",
    )
    operator: Literal[
        "contains",
        "equals",
        "notContains",
        "notEquals",
        "includingRegex",
        "excludingRegex",
    ] = Field(
        "equals",
        description="How your specified value must match (or not match) the dimension value. 'contains': row value contains or equals expression (non-case-sensitive). 'equals': [Default] exact match (case-sensitive for page and query). 'notContains': row value must not contain expression. 'notEquals': must not exactly equal. 'includingRegex': RE2 regex that must match. 'excludingRegex': RE2 regex that must not match.",
    )
    expression: str = Field(
        ...,
        description="The value for the filter to match or exclude, depending on the operator. Max length 4096 characters.",
    )


class DimensionFilterGroup(BaseModel):
    """A group of filters to apply to the dimension grouping values."""

    groupType: Literal["and"] = Field(
        "and",
        description="Whether all filters in this group must return true ('and'), or one or more must return true (not yet supported). Acceptable value: 'and' (all filters must return true).",
    )
    filters: List[DimensionFilter] = Field(
        default_factory=list,
        description="Zero or more filters to test against the row. Each filter consists of a dimension name, an operator, and a value. Examples: country equals FRA; query contains mobile use; device notContains tablet.",
    )


class SearchAnalysisRequest(BaseModel):
    """Request parameters for search analysis query."""

    siteUrl: str = Field(
        ...,
        description="The site's URL, including protocol. For a URL-prefix property, supply the full URL (e.g. 'https://www.example.com/'). For a domain property, supply 'sc-domain:example.com'.",
    )
    startDate: str = Field(
        ...,
        description="Start date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be less than or equal to the end date. This value is included in the range.",
    )
    endDate: str = Field(
        ...,
        description="End date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be greater than or equal to the start date. This value is included in the range.",
    )
    dimensions: List[str] | None = Field(
        None,
        description="Zero or more dimensions to group results by. Results are grouped in the order that you supply these dimensions. You can use any dimension name in dimensionFilterGroups[].filters[].dimension as well as date and hour. The grouping dimension values are combined to create a unique key for each result row. If no dimensions are specified, all values will be combined into a single row. There is no limit to the number of dimensions that you can group by, but you cannot group by the same dimension twice. Example: [country, device]",
    )
    type: Literal["discover", "googleNews", "news", "image", "video", "web"] | None = Field(
        None,
        description="Filter results to the following type: discover: Discover results; googleNews: Results from news.google.com and the Google News app on Android and iOS. Doesn't include results from the News tab in Google Search., news: Search results from the News tab in Google Search., image: Search results from the Image tab in Google Search.; video: Video search results; web: [Default] Filter results to the combined (All) tab in Google Search. Does not include Discover or Google News results.",
    )
    dimensionFilterGroups: List[DimensionFilterGroup] | None = Field(
        None,
        description="Zero or more groups of filters to apply to the dimension grouping values. All filter groups must match in order for a row to be returned in the response. Within a single filter group, you can specify whether all filters must match, or at least one must match.",
    )
    aggregationType: Literal["auto", "byNewsShowcasePanel", "byPage", "byProperty"] | None = Field(
        None,
        description="How data is aggregated. 'auto': [Default] let the service decide. 'byNewsShowcasePanel': aggregate by News Showcase panel (requires the NEWS_SHOWCASE searchAppearance filter and type=discover or type=googleNews). 'byPage': aggregate by URI. 'byProperty': aggregate by property (not supported for type=discover or type=googleNews). Note: if you group or filter by page, you cannot aggregate by property.",
    )
    rowLimit: int | None = Field(
        None,
        ge=1,
        le=25000,
        description="The maximum number of rows to return. Valid range is 1-25,000; default is 1,000. To page through results, use the startRow offset.",
    )
    startRow: int | None = Field(
        None,
        ge=0,
        description="Zero-based index of the first row in the response. Must be a non-negative number. Default is 0. If startRow exceeds the number of results for the query, the response will be a successful response with zero rows.",
    )
    dataState: Literal["all", "final", "hourly_all"] | None = Field(
        None,
        description="If 'all' (case-insensitive), data will include fresh data. If 'final' (case-insensitive) or if omitted, the returned data will include only finalized data. If 'hourly_all' (case-insensitive), data will include an hourly breakdown; this indicates that hourly data includes partial data and should be used when grouping by the HOUR API dimension.",
    )

class SitemapRequestParams(BaseModel):
    feedpath: str = Field(..., description="The URL of the actual sitemap. For example: http://www.example.com/sitemap.xml")
    siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/")

class ListSitemapRequestParams(BaseModel):
    siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/")
    sitemapIndex: Optional[str] = Field(None, description="A URL of a site's sitemap index. For example: http://www.example.com/sitemapindex.xml")

class SiteRequestParams(BaseModel):
    siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. For example: http://www.example.com/")

class IndexInspectRequestBody(BaseModel):
    inspectionUrl: str = Field(..., description="Fully-qualified URL to inspect. Must be under the property specified in 'siteUrl'.")
    siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. Note that URL-prefix properties must include a trailing / mark. Examples: https://www.example.com/ for a URL-prefix property, or sc-domain:example.com for a Domain property.")
    languageCode: Optional[str] = Field(None, description="An IETF BCP-47 language code representing the requested language for translated issue messages, e.g.'en-US', or 'de-CH'. Default value is 'en-US'.")
