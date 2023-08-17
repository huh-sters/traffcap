import logging
from traffcap.core import log_setup


def test_it_adjusts_logging_levels():
    """
    Make sure the logging levels are adjusted
    """
    log_setup()
    root = logging.getLogger()
    gunicorn_logger = logging.getLogger("gunicorn")
    access_logger = logging.getLogger("gunicorn.access")
    sqlalchemy_logger = logging.getLogger("sqlalchemy")

    assert root.getEffectiveLevel() == logging.INFO
    assert gunicorn_logger.getEffectiveLevel() == logging.ERROR
    assert access_logger.getEffectiveLevel() == logging.INFO
    assert sqlalchemy_logger.getEffectiveLevel() == logging.ERROR
