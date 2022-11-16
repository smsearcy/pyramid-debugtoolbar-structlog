from __future__ import annotations

import threading

import structlog
from pyramid_debugtoolbar.panels import DebugPanel


class DebugPanelProcessor:
    """Save logged event dictionaries, per thread."""

    # based on pyramid_debugtoolbar.panels.logger.ThreadTrackingHandler()
    def __init__(self):
        self.records: dict[threading.Thread, list[tuple[str, dict]]] = {}

    def __call__(self, logger, log_method, event_dict):
        self.get_records().append((log_method, event_dict.copy()))
        return event_dict

    def get_records(self, thread: threading.Thread | None = None):
        """Get list of records for a particular thread.

        Uses the current thread unless ``thread`` is provided.
        """
        if thread is None:
            thread = threading.current_thread()
        return self.records.setdefault(thread, [])

    def clear_records(self, thread: threading.Thread | None = None):
        """Clear list of records for a particular thread.

        Uses the current thread unless ``thread`` is provided.
        """
        if thread is None:
            thread = threading.current_thread()
        if thread in self.records:
            del self.records[thread]


# add processor to the configured processors
structlog_config = structlog.get_config()
panel_processor = DebugPanelProcessor()
processors = structlog_config["processors"]
processors[-1:-1] = [panel_processor]
structlog.configure(processors=processors)


class StructLogDebugPanel(DebugPanel):
    """Panel for capturing `structlog` messages.

    Necessary if `structlog` isn't using `logging` for output.
    """

    name = "structlog"
    template = "pyramid_debugtoolbar_structlog.panels:templates/structlog.dbtmako"

    def __init__(self, request):
        panel_processor.clear_records()
        self.data = {"records": []}

    def process_response(self, response):
        records = panel_processor.get_records()
        panel_processor.clear_records()
        messages = []
        for log_method, event_dict in records:
            event = event_dict.pop("event", "")
            messages.append(
                {
                    "method": log_method,
                    "event": event,
                    "context": event_dict,
                }
            )
        self.data = {"records": messages}

    @property
    def nav_title(self):
        return "structlog"

    @property
    def title(self):
        return "Structured Logging"

    @property
    def has_content(self):
        return bool(self.data["records"])
