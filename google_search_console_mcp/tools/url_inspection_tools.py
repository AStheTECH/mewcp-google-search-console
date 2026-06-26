"""URL Inspection group: inspect_index."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import IndexInspectData, IndexInspectResult, IndexInspectRequestBody
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
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def inspect_index(body: IndexInspectRequestBody) -> IndexInspectResult:
        tlog = ToolLogger(logger, "inspect_index")

        try:
            svc = service.get_service()
            result = (
                svc.urlInspection()
                .index()
                .inspect(body=body.model_dump(exclude_none=True))
                .execute()
            )
            tlog.success()
            return IndexInspectResult(success=True, statusCode=200, data=IndexInspectData(**result))

        except Exception as exc:
            return _handle_sdk_exc(IndexInspectResult, tlog, exc)
