import logging
import os
from logging.handlers import TimedRotatingFileHandler

class Logger:
    def __init__(self, app_name, log_path, log_level):
        self.logger = logging.getLogger(app_name)
        log_file = os.path.join(log_path, f"{app_name}.log")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        handler = TimedRotatingFileHandler(filename=log_file, when="midnight")
        handler.suffix = "%Y_%m_%d"
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        self.logger.setLevel(self._resolve_log_level(log_level))

    def _resolve_log_level(self, log_level):
        return getattr(logging, log_level.upper())
