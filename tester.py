import os
import time
from pathlib import Path
from bs4 import BeautifulSoup

from main import load_directory_paths
from utils.utils import remove_tags, get_all_questions


def main():
    pass
    directories = load_directory_paths()
    raw_html_dir = Path(directories["raw_html"])

    # file_to_parse = os.path.join(raw_html_dir, "CEN 4078  Chapter 9 Quiz.html")
    file_to_parse = os.path.join(raw_html_dir, "CEN 4078 Chapter 6 Quiz.html")
    # file_to_parse = os.path.join(raw_html_dir, "CEN 4078 Chapter 9 Quiz_ BEFORE ANSWERS.html")
    # file_to_parse = os.path.join(raw_html_dir, "Quiz 1- Requires Respondus LockDown Browser.html")

    with open(file_to_parse, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = remove_tags(html_content)
    questions_list = get_all_questions(soup)
    print(len(questions_list))


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
