"""Shared error helpers for all tool modules."""

from googleapiclient.errors import HttpError

from ..logging_utils import ToolLogger  # noqa: F401  (re-exported for tool modules)
from ..schemas import ToolError


def _err(result_class, tlog, code, message, status, retriable=False, retry_after=None):
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_sdk_exc(result_class, tlog, exc):
    if isinstance(exc, HttpError):
        status = int(exc.resp.status)
        retriable = status in (429, 500, 502, 503)
        tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
        return result_class(
            success=False, statusCode=status, retriable=retriable,
            error=ToolError(code="UPSTREAM_ERROR", message=f"HTTP {status}"),
        )
    if isinstance(exc, ValueError):
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message=str(exc)))