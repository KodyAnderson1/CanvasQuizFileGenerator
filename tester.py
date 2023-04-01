import argparse
import os
import shutil
import yaml
from pathlib import Path
from typing import Optional, Dict
from bs4 import BeautifulSoup
import time

from main import find_div_by_id, count_aria_labels
from utils.processor import ProcessQuestions, get_question_text, find_elements_by_class
from utils.quiz import Quiz, QuizFileGenerator, MultipleShortAnswerQuestion


def load_directory_paths() -> Dict[str, str]:
    with open("configurations.yaml", "r") as f:
        paths = yaml.safe_load(f)
    return paths["directory_paths"]


def main():
    directories = load_directory_paths()
    raw_html_dir = Path(directories["raw_html"])

    # file_to_parse = os.path.join(raw_html_dir, "Quiz 1- Requires Respondus LockDown Browser.html")
    file_to_parse = os.path.join(raw_html_dir, "Homework 3 Results for Anthony Welter.html")

    with open(file_to_parse, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    # print(count_aria_labels(find_div_by_id(soup, "questions"), "Question"))

    for stuff in process_multiple_short_answer(soup):
        print(stuff)
        print()


def process_multiple_short_answer(soup: BeautifulSoup) -> list[MultipleShortAnswerQuestion]:
    """
    Processes a multiple short answer question.

    :param soup: The BeautifulSoup object containing the question.
    :return: A list containing the question and the answers.
    """
    return [MultipleShortAnswerQuestion(question=get_question_text(div),
                                        answers=[])
            for div in find_elements_by_class(soup, "fill_in_multiple_blanks_question")]


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
