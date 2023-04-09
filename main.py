import argparse
import itertools
import json
import logging
import os
import shutil
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import Dict

import yaml
from bs4 import BeautifulSoup

from utils import log_config
from utils.processor import process_html
from utils.quiz import Quiz
from utils.quiz_writer import QuizWriter


def load_directory_paths() -> Dict[str, str]:
    with open("configurations.yaml", "r") as f:
        paths = yaml.safe_load(f)
    return paths["directory_paths"]


def create_output_directories(directories: dict) -> None:
    for _, path in directories.items():
        if not os.path.exists(path):
            os.makedirs(path)


def read_html_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content


def parse_html(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def process_json_file(json_file: Path) -> Quiz:
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)
    return Quiz.from_json(json_data)


def process_single_file(args, raw_html_file: Path, output_dir: Path, parsed_html_dir: Path) -> str:
    html_content = read_html_file(raw_html_file)

    quiz = process_html(html_content)
    wq = QuizWriter(quiz)

    output_file = output_dir / f"{quiz.title}"
    try:
        wq.write(args.file_type, output_file)

        new_html_file = parsed_html_dir / f"{quiz.title}.html"
        if args.remove_html:
            os.remove(raw_html_file)
        elif args.dont_move:
            pass
        else:
            shutil.move(raw_html_file, new_html_file)

    except Exception as ex:
        logging.exception(ex)
        logging.info(f"Error occurred while writing {raw_html_file}. Skipping...")

    return f"Processed {raw_html_file} and saved output as {output_file}.{args.file_type}"


# def merge_quizzes(args, quiz_chunks: list) -> Quiz:
#     merged_quiz = quiz_chunks[0]
#     for quiz in quiz_chunks[1:]:
#         merged_quiz = combine_quizzes(merged_quiz, quiz)
#     return merged_quiz

def merge_quizzes(args, quiz_chunks: list) -> Quiz:
    merged_quiz = quiz_chunks[0]
    for quiz in quiz_chunks[1:]:
        merged_quiz = merged_quiz.combine(quiz)
    return merged_quiz


def combine_quizzes_from_files(args, quizzes, output_dir: Path) -> None:
    # Split quizzes into chunks for parallel processing
    chunk_size = max(len(quizzes) // args.cores, 1)
    quiz_chunks = [quizzes[i:i + chunk_size] for i in range(0, len(quizzes), chunk_size)]

    # Process each chunk in parallel and combine the results
    with ProcessPoolExecutor(max_workers=args.cores) as executor:
        merged_quiz_chunks = list(executor.map(merge_quizzes, itertools.repeat(args), quiz_chunks))

    combined_quiz = merge_quizzes(args, merged_quiz_chunks)

    wq = QuizWriter(combined_quiz)
    output_file = output_dir / f"combined_quiz"
    wq.write(args.file_type, output_file)


def process_files(args, directories: dict) -> None:
    raw_html_dir = Path(directories["raw_html"])
    parsed_html_dir = Path(directories["parsed_html"])
    output_dir = Path(directories["output"])

    if args.search_json:
        file_extension = "*.json"
    else:
        file_extension = "*.html"

    quizzes = []

    for file in raw_html_dir.glob(file_extension):
        if args.search_json:
            quiz = process_json_file(file)
        else:
            html_content = read_html_file(file)
            quiz = process_html(html_content)
        quizzes.append(quiz)

    if args.combine:
        combine_quizzes_from_files(args, quizzes, output_dir)
    else:
        with ProcessPoolExecutor(max_workers=args.cores) as executor:
            process_file_with_args = \
                partial(process_single_file, args, output_dir=output_dir, parsed_html_dir=parsed_html_dir)

            results = list(executor.map(process_file_with_args, raw_html_dir.glob(file_extension)))

        for result in results:
            print(result)


def main():
    file_choices = ["txt", "json", "yaml", "md", "qz.txt"]
    default_file = "qz.txt"

    parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")
    parser.add_argument(
        "-f", "--file_type", type=str, default=default_file, nargs="+",
        choices=file_choices,
        help=f"File type to save the quiz as. Options: {', '.join(file_choices)}."
    )

    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        "-rm", "--remove_html", action="store_true",
        help="Remove HTML files instead of renaming and moving them. Cannot use with -dm flag."
    )

    exclusive_group.add_argument(
        "-dm", "--dont_move", action="store_true",
        help="Keep .html files in origin directory with original names. Cannot use with -rm flag."
    )

    parser.add_argument(
        "-c", "--cores", type=int, default=os.cpu_count() // 2,
        help="Number of CPU cores for processing. Default is half the available cores."
    )

    parser.add_argument(
        "-sj", "--search_json", action="store_true",
        help="Search for JSON files instead of HTML and combine all quiz objects represented."
    )

    parser.add_argument(
        "-cb", "--combine", action="store_true",
        help="Combine all quizzes found into one quiz item."
    )

    args = parser.parse_args()

    # Ensure the number of cores is between 1 and the total number of cores
    args.cores = max(min(args.cores, os.cpu_count()), 1)

    directories = load_directory_paths()

    create_output_directories(directories)

    process_files(args, directories)


if __name__ == '__main__':
    start_time = time.time()

    try:
        # cProfile.run('main()', filename='my_results.prof')
        main()
    except Exception as e:
        logging.exception(e)
        logging.info("An error occurred. Please check the log file for more details.")

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
