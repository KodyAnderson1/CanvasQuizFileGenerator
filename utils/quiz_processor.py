import json
import logging
import os
import shutil

from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path

from utils.parser import process_html
from utils.quiz import Quiz
from utils.quiz_writer import QuizWriter


class QuizProcessor:
    def __init__(self, args, directories):
        self.args = args
        self.directories = directories
        self.raw_html_dir = Path(self.directories["raw_html"])
        self.parsed_html_dir = Path(self.directories["parsed_html"])
        self.output_dir = Path(self.directories["output"])

        self.file_extension = "*.json" if self.args.search_json else "*.html"

        self.quizzes = []

    def _process_file(self, file):
        if self.args.search_json:
            return self.process_json_file(file)
        elif self.args.combine and not self.args.search_json:
            html_content = self.read_html_file(file)
            return process_html(html_content)

        # logging.critical("Invalid combination of arguments. _process_file() should not be called.")

    def process_files(self):
        with ProcessPoolExecutor(max_workers=self.args.cores) as executor:
            process_file_with_args = partial(self._process_file)
            futures = {executor.submit(process_file_with_args, file): file for file in
                       self.raw_html_dir.glob(self.file_extension)}

            for future in as_completed(futures):
                result = future.result()
                self.quizzes.append(result)

        if self.args.combine:
            self.combine_quizzes_from_files()
        elif self.args.search_json:  # Code here to print JSON into w/e other format wanted
            pass
        else:
            self.process_files_parallel()

    def merge_quizzes(self, quiz_chunks: list) -> Quiz:
        merged_quiz = quiz_chunks[0]
        for quiz in quiz_chunks[1:]:
            merged_quiz = merged_quiz.combine(quiz)
        return merged_quiz

    def process_files_parallel(self):
        with ProcessPoolExecutor(max_workers=self.args.cores) as executor:
            process_file_with_args = \
                partial(self.process_single_file, output_dir=self.output_dir, parsed_html_dir=self.parsed_html_dir)
            results = list(executor.map(process_file_with_args, self.raw_html_dir.glob(self.file_extension)))

        for result in results:
            print(result)

    def combine_quizzes_from_files(self):
        chunk_size = max(len(self.quizzes) // self.args.cores, 1)
        quiz_chunks = [self.quizzes[i:i + chunk_size] for i in range(0, len(self.quizzes), chunk_size)]

        with ProcessPoolExecutor(max_workers=self.args.cores) as executor:
            merged_quiz_chunks = list(executor.map(self.merge_quizzes, quiz_chunks))

        combined_quiz = self.merge_quizzes(merged_quiz_chunks)

        wq = QuizWriter(combined_quiz)
        output_file = self.output_dir / f"combined_quiz"
        wq.write(self.args.file_type, output_file)

    def process_single_file(self, raw_html_file: Path, output_dir: Path, parsed_html_dir: Path) -> str:
        html_content = self.read_html_file(raw_html_file)

        quiz = process_html(html_content)
        wq = QuizWriter(quiz)

        output_file = output_dir / f"{quiz.title}"
        try:
            wq.write(self.args.file_type, output_file)

            new_html_file = parsed_html_dir / f"{quiz.title}.html"
            if self.args.remove_html:
                os.remove(raw_html_file)
            elif self.args.dont_move:
                pass
            else:
                shutil.move(raw_html_file, new_html_file)

        except Exception as ex:
            logging.exception(ex)
            logging.info(f"Error occurred while writing {raw_html_file}. Skipping...")

        return f"Processed {raw_html_file} and saved output as {output_file}.{self.args.file_type}"

    def process_json_file(self, json_file: Path) -> Quiz:
        with open(json_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)
        return Quiz.from_json(json_data)

    def read_html_file(self, file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return html_content
