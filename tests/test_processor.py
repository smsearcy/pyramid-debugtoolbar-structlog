from threading import Thread

from pyramid_debugtoolbar_structlog.panels.structlog_ import DebugPanelProcessor


def test_thread_dictionary():
    """Verify that the log processor is keeping track of entries per thread."""
    processor = DebugPanelProcessor()
    thread = Thread()

    for t in (thread, None):
        assert processor.get_records(t) == []

    processor(None, "info", {"foo": "bar"})
    assert processor.get_records() == [("info", {"foo": "bar"})]
    assert processor.get_records(thread) == []

    for t in (thread, None):
        processor.clear_records(t)

    for t in (thread, None):
        assert processor.get_records(t) == []
