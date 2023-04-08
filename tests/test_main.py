import os
from argparse import Namespace
from pathlib import Path

from bs4 import BeautifulSoup

import main

EXPECTED_TEXT_DIR = Path("tests", "test_files", "expected_text")
OUTPUT_TEXT_DIR = Path("tests", "test_files", "output_text")
HTML_DIR = Path("tests", "html")

TEST_DICTIONARY = {
    "raw_html": HTML_DIR,
    "output": OUTPUT_TEXT_DIR,
    "parsed_html": HTML_DIR
}


def test_process_files():
    print(os.getcwd())
    main.process_files(Namespace(file_type='txt', remove_html=False, dont_move=True), TEST_DICTIONARY)
    for expected_file in EXPECTED_TEXT_DIR.glob("*.txt"):
        expected_text = expected_file.read_text()
        output_file = OUTPUT_TEXT_DIR / expected_file.name
        output_text = output_file.read_text()
        print(f"TEXT DOES NOT MATCH: EXPECTED: {expected_file} ACTUAL: {output_file}")
        assert expected_text == output_text
        if expected_text == output_text:
            output_file.unlink()  # Delete the output file if the assertion is successful
        else:
            print(f"TEXT DOES NOT MATCH: EXPECTED: {expected_text} ACTUAL: {output_text}")


def test_parse_html():
    html_content = "<html><head><title>Test HTML</title></head><body><p>Test paragraph</p></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")
    assert main.parse_html(html_content).prettify() == soup.prettify()


def test_create_directories(tmp_path):
    directories = {
        "test_dir1": tmp_path / "test_dir1",
        "test_dir2": tmp_path / "test_dir2",
    }
    main.create_directories(directories)

    for directory in directories.values():
        assert directory.exists()

    # remove the directories
    for directory in directories.values():
        os.rmdir(directory)


def test_read_html_file(tmp_path):
    test_file = tmp_path / "test.html"
    with open(test_file, "w") as f:
        f.write("Test HTML file")
    assert main.read_html_file(test_file) == "Test HTML file"

    # Remove the file
    os.remove(test_file)
