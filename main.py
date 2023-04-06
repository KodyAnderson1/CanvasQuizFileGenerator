import argparse
import os
import shutil
import yaml
from pathlib import Path
from typing import Optional, Dict
from bs4 import BeautifulSoup
import time

from utils.processor import ProcessQuestions
from utils.quiz import Quiz, QuizWriter

"""
multiple_dropdowns_question (HW3)

"""


def load_directory_paths() -> Dict[str, str]:
    with open("configurations.yaml", "r") as f:
        paths = yaml.safe_load(f)
    return paths["directory_paths"]


def create_directories(directories: dict) -> None:
    for k, v in directories.items():
        if not os.path.exists(v):
            os.makedirs(v)


def find_quiz_title(soup: BeautifulSoup) -> Optional[str]:
    title_tag = soup.find("h1", id="quiz_title")
    if not title_tag:
        title_tag = soup.find("header", class_="quiz-header").find("h2")
    return title_tag.text.strip() if title_tag else None


def find_div_by_id(soup: BeautifulSoup, id_attr: str) -> Optional[BeautifulSoup]:
    return soup.find("div", id=id_attr)


def count_aria_labels(soup: BeautifulSoup, label_name: str) -> Optional[int]:
    return len(soup.find_all(attrs={"aria-label": label_name})) if soup else None


def read_html_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content


def parse_html(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def process_quiz(soup: BeautifulSoup) -> Quiz:
    quiz = Quiz()

    quiz.title = find_quiz_title(soup)
    questions_div = find_div_by_id(soup, "questions")
    quiz.number_of_questions = count_aria_labels(questions_div, "Question")

    processor = ProcessQuestions(soup)

    quiz.multiple_choice_questions = processor.process_multiple_choice()
    quiz.matching_questions = processor.process_matching()
    quiz.multiple_answer_questions = processor.process_multiple_answers()
    quiz.multiple_short_answer_questions = processor.process_multiple_short_answers()

    return quiz


def process_files(args, directories: dict) -> None:
    raw_html_dir = Path(directories["raw_html"])
    parsed_html_dir = Path(directories["parsed_html"])
    output_dir = Path(directories["output"])

    for raw_html_file in raw_html_dir.glob("*.html"):
        html_content = read_html_file(raw_html_file)
        soup = parse_html(html_content)
        quiz = process_quiz(soup)

        wq = QuizWriter(quiz)
        output_file = output_dir / f"{quiz.title}"
        wq.write(args.file_type, output_file)

        new_html_file = parsed_html_dir / f"{quiz.title}.html"
        if args.remove_html:
            os.remove(raw_html_file)
        elif args.dont_move:
            pass
        else:
            shutil.move(raw_html_file, new_html_file)

        print(f"Processed {raw_html_file} and saved output as {output_file}.{args.file_type}")


def main():
    parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")
    parser.add_argument(
        "-f", "--file_type", type=str, default="qz.txt", nargs="+",
        choices=["txt", "json", "yaml", "md", "qz.txt"],
        help="The file type to save the quiz as. Options: txt, md, json, yaml, qz.txt."
    )

    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        "-rm", "--remove_html", action="store_true",
        help="Flag to remove the HTML files instead of renaming and moving them. "
             "Selecting this flag will prevent the use of the -dm flag."
    )

    exclusive_group.add_argument(
        "-dm", "--dont_move", action="store_true",
        help="Flag to keep .html files in the origin directory with their original names. "
             "Selecting this flag will prevent the use of the -rm flag."
    )

    args = parser.parse_args()

    directories = load_directory_paths()

    create_directories(directories)

    process_files(args, directories)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
