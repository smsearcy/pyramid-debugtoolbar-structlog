import pytest
import structlog

from pyramid_debugtoolbar_structlog.panels import structlog_ as structlog_panel

logger = structlog.get_logger()


@pytest.fixture
def processor():
    """Ensure an empty log processor for each test."""
    structlog_panel.panel_processor.clear_records()


def test_config(processor):
    """Verify that our log processor is inserted into structlog's processors."""

    logger.info("event", context="foo")

    method, event_dict = structlog_panel.panel_processor.get_records()[0]
    # structlog processors add extra information, so cannot do equality check
    assert method == "info"
    assert event_dict["event"] == "event"
    assert event_dict["context"] == "foo"
