import logging
import os
import sys
from datetime import date


class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=1500, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.current_date = date.today()
        self.new_day = True

    def emit(self, record):
        # Check if it's a new day
        today = date.today()
        if today != self.current_date:
            self.current_date = today
            self.new_day = True

        # Check if the log file has reached the maximum number of lines
        if sum(1 for _ in open(self.baseFilename)) >= self.max_lines:
            self.close()
            os.remove(self.baseFilename)
            self.stream = self._open()

        # Add a custom heading for the new day
        if self.new_day:
            self.stream.write(f"Log entries for {self.current_date}:\n")
            self.new_day = False

        super().emit(record)


def setup_logging():
    # Create a logs directory if it doesn't exist
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    # Set up the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Set up the formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set up the console handler for debug and info messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Set up the custom file handler for warning, error, and critical messages
    file_handler = CustomFileHandler('./logs/logfile.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Set up logging when the module is imported
setup_logging()
