from gunicorn.app.base import BaseApplication
from fastapi import FastAPI


# Class for running FastAPI from within Python itself
class StandaloneApplication(BaseApplication):
    def __init__(self, app: FastAPI, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> FastAPI:
        return self.application
