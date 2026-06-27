"""URL Inspection group: inspect_index."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import IndexInspectData, IndexInspectResult
from ._helpers import _handle_sdk_exc

logger = logging.getLogger("google-search-console-mcp.tools.url_inspection")


def register_url_inspection_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="inspect_index",
        description=(
            "View the indexed, or indexable, status of the provided URL. "
            "Presently only the status of the version in the Google index is available; "
            "you cannot test the indexability of a live URL."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def inspect_index(
        inspectionUrl: str = Field(..., description="Fully-qualified URL to inspect. Must be under the property specified in 'siteUrl'."),
        siteUrl: str = Field(..., description="The URL of the property as defined in Search Console. Note that URL-prefix properties must include a trailing / mark. Examples: https://www.example.com/ for a URL-prefix property, or sc-domain:example.com for a Domain property."),
        languageCode: str | None = Field(None, description="An IETF BCP-47 language code representing the requested language for translated issue messages, e.g.'en-US', or 'de-CH'. Default value is 'en-US'."),
    ) -> IndexInspectResult:
        tlog = ToolLogger(logger, "inspect_index")

        try:
            svc = service.get_service()
            body = {"inspectionUrl": inspectionUrl, "siteUrl": siteUrl}
            if languageCode is not None:
                body["languageCode"] = languageCode
            result = (
                svc.urlInspection()
                .index()
                .inspect(body=body)
                .execute()
            )
            tlog.success()
            return IndexInspectResult(success=True, statusCode=200, data=IndexInspectData(**result))

        except Exception as exc:
            return _handle_sdk_exc(IndexInspectResult, tlog, exc)
