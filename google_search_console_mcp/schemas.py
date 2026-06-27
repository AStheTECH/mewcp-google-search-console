from typing import Any, Literal, List
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Base classes
# ---------------------------------------------------------------------------

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# ---------------------------------------------------------------------------
# Nested models (used as parameter types in tool signatures)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Per-tool data + result models
# ---------------------------------------------------------------------------

class SearchAnalysisData(BaseModel):
    model_config = ConfigDict(extra="allow")

    rows: list = []
    responseAggregationType: str | None = None


class SearchAnalysisResult(ToolResult):
    data: SearchAnalysisData | None = None


class DeleteSitemapData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool
    message: str | None = None


class DeleteSitemapResult(ToolResult):
    data: DeleteSitemapData | None = None


class SitemapData(BaseModel):
    model_config = ConfigDict(extra="allow")

    path: str | None = None
    lastSubmitted: str | None = None
    isPending: bool | None = None
    isSitemapsIndex: bool | None = None
    type: str | None = None
    lastDownloaded: str | None = None
    warnings: int | None = None
    errors: int | None = None
    contents: list | None = None


class SitemapResult(ToolResult):
    data: SitemapData | None = None


class SitemapListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    sitemap: list | None = None


class SitemapListResult(ToolResult):
    data: SitemapListData | None = None


class SubmitSitemapData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool
    message: str | None = None


class SubmitSitemapResult(ToolResult):
    data: SubmitSitemapData | None = None


class AddSiteData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool
    message: str | None = None


class AddSiteResult(ToolResult):
    data: AddSiteData | None = None


class DeleteSiteData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool
    message: str | None = None


class DeleteSiteResult(ToolResult):
    data: DeleteSiteData | None = None


class SiteData(BaseModel):
    model_config = ConfigDict(extra="allow")

    siteUrl: str | None = None
    permissionLevel: str | None = None


class SiteResult(ToolResult):
    data: SiteData | None = None


class SiteListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    siteEntry: list | None = None


class SiteListResult(ToolResult):
    data: SiteListData | None = None


class IndexInspectData(BaseModel):
    model_config = ConfigDict(extra="allow")

    inspectionResult: dict | None = None


class IndexInspectResult(ToolResult):
    data: IndexInspectData | None = None
