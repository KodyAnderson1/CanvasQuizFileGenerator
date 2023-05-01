import logging
import os
import sys
import json
from datetime import date

import yaml

with open("configurations.yaml", "r") as f:
    paths = yaml.safe_load(f)


class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=1500, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.current_date = date.today()
        self.new_day = True

    def emit(self, record):
        # Check if the log file has reached the maximum number of lines
        if sum(1 for _ in open(self.baseFilename)) >= self.max_lines:
            self.close()
            os.remove(self.baseFilename)
            self.stream = self._open()

        super().emit(record)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'filename': record.filename,
            'funcName': record.funcName,
            'lineno': record.lineno,
            'processName': record.processName,
            'message': record.getMessage()
        }
        return json.dumps(log_entry)


def setup_logging():
    log_path = paths["directory_paths"]['logs']
    # Create a logs directory if it doesn't exist
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Set up the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Set up the JSON formatter
    formatter = JsonFormatter()

    # Set up the console handler for debug and info messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Set up the custom file handler for warning, error, and critical messages
    file_handler = CustomFileHandler(os.path.join(log_path, "logfile.log"))

    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Set up logging when the module is imported
setup_logging()
