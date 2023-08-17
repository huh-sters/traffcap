import logging
from traffcap.core import banner


def test_it_logs_a_banner(caplog):
    """
    Banner function needs to output something
    """
    caplog.set_level(logging.INFO)
    banner()
    assert caplog.text != ""
