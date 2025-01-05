import sys
import logging


def log_setup() -> None:
    """
    Attach stdio to the logging pipeline
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    gunicorn_logger = logging.getLogger("gunicorn")
    gunicorn_logger.setLevel(logging.DEBUG)
    gunicorn_handler = logging.StreamHandler(sys.stdout)
    gunicorn_logger.addHandler(gunicorn_handler)

    access_logger = logging.getLogger("gunicorn.access")
    access_logger.setLevel(logging.DEBUG)
    access_handler = logging.StreamHandler(sys.stdout)
    access_logger.addHandler(access_handler)

    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.setLevel(logging.DEBUG)
    sqlalchemy_handler = logging.StreamHandler(sys.stdout)
    sqlalchemy_logger.addHandler(sqlalchemy_handler)
