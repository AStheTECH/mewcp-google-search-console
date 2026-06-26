from __future__ import annotations
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ToolLogger:
    def __init__(self, logger: logging.Logger, tool: str) -> None:
        self._log = logger
        self._tool = tool
        self._start = time.monotonic()
        self._log.info("tool=%s status=started", self._tool)

    def _ms(self) -> int:
        return round((time.monotonic() - self._start) * 1000)

    def success(self) -> None:
        self._log.info(
            "tool=%s status=ok duration_ms=%d",
            self._tool, self._ms(),
        )

    def failure(self, code: str, message: str) -> None:
        self._log.error(
            "tool=%s status=error code=%s duration_ms=%d msg=%s",
            self._tool, code, self._ms(), message,
        )
