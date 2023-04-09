from pathlib import Path
import json
from typing import Dict

from bs4 import BeautifulSoup
import yaml

from utils.quiz import Quiz


def read_html_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content


def parse_html(html_content: str) -> BeautifulSoup:
    return BeautifulSoup(html_content, "html.parser")


def process_json_file(json_file: Path) -> Quiz:
    with json_file.open("r", encoding="utf-8") as file:
        json_data = json.load(file)
    return Quiz.from_json(json_data)


def load_directory_paths() -> Dict[str, str]:
    with open("configurations.yaml", "r") as f:
        paths = yaml.safe_load(f)
    return paths["directory_paths"]


def create_output_directories(directories: dict) -> None:
    for _, path in directories.items():
        Path(path).mkdir(parents=True, exist_ok=True)
