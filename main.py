import argparse
import cProfile
import logging
import os
import time
from typing import Dict
import yaml

from utils import log_config

from utils.quiz_processor import QuizProcessor


class QuizProcessorMain:
    def __init__(self):
        self.file_choices = ["txt", "json", "yaml", "md", "qz.txt"]
        self.default_file = "qz.txt"

        self.parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")
        self.parser.add_argument("-f", "--file_type", type=str, default=self.default_file, nargs="+",
                                 choices=self.file_choices,
                                 help=f"File type to save the quiz. Options: {', '.join(self.file_choices)}.")
        self.parser.add_argument("-c", "--cores", type=int, default=os.cpu_count() // 2,
                                 help="Number of CPU cores for processing. Default is half the available cores.")
        self.parser.add_argument("-sj", "--search_json", action="store_true",
                                 help="Search for JSON files instead of HTML and combine all quiz objects represented.")
        self.parser.add_argument("-cb", "--combine", action="store_true",
                                 help="Combine all quizzes found into one quiz item.")

        exclusive_group = self.parser.add_mutually_exclusive_group()
        exclusive_group.add_argument("-rm", "--remove_html", action="store_true",
                                     help="Remove HTML files instead of renaming and moving them. Cannot use with -dm flag.")
        exclusive_group.add_argument("-dm", "--dont_move", action="store_true",
                                     help="Keep .html files in origin directory with original names. Cannot use with -rm flag.")

        self.args = self.parser.parse_args()

        # Ensure the number of cores is between 1 and the total number of cores
        self.args.cores = max(min(self.args.cores, os.cpu_count()), 1)

        self.directories = self.load_directory_paths()

        self.create_output_directories()

    def load_directory_paths(self) -> Dict[str, str]:
        with open("configurations.yaml", "r") as f:
            paths = yaml.safe_load(f)
        return paths["directory_paths"]

    def create_output_directories(self) -> None:
        for _, path in self.directories.items():
            if not os.path.exists(path):
                os.makedirs(path)

    def main(self):
        quiz_processor = QuizProcessor(self.args, self.directories)
        quiz_processor.process_files()


if __name__ == '__main__':
    start_time = time.time()

    try:
        quiz_processor_main = QuizProcessorMain()
        quiz_processor_main.main()
        # cProfile.run('quiz_processor_main.main()', filename='my_results.prof')
    except Exception as e:
        logging.exception(e)
        logging.info("An error occurred. Please check the log file for more details.")

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
