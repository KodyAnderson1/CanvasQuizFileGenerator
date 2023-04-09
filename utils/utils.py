import re
import uuid
from html import unescape
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

NO_ANSWER = "CANNOT DETERMINE ANSWER. PLEASE CHECK MANUALLY."


def get_all_questions(soup: BeautifulSoup = None) -> List[BeautifulSoup]:
    return soup.find_all('div', {'aria-label': 'Question'})


def clean_input(input_obj):
    def clean_str(s: str) -> str:
        return ' '.join(s.strip().split())

    def clean_dict(d: dict) -> dict:
        return {k.strip(): v.strip() for k, v in d.items() if v.strip()}

    def clean_list(l: list) -> list:
        return remove_duplicates([clean_str(item) for item in l if item.strip()])

    cleaning_functions = {
        str: clean_str,
        dict: clean_dict,
        list: clean_list,
    }

    cleaning_function = cleaning_functions.get(type(input_obj))
    return cleaning_function(input_obj) if cleaning_function else input_obj


def remove_duplicates(input_list) -> List:
    seen = set()
    return [x for x in input_list if not (x in seen or seen.add(x))]


def clean_html(html_string) -> str:
    """
    Cleans an HTML string by removing img tags, replacing input tags with a placeholder, and removing &nbsp; entities.

    :param html_string: The HTML string to clean.
    :return: The cleaned HTML string.
    """
    if not isinstance(html_string, Tag) or html_string.text == '':
        return html_string

    # Parse the HTML string with Beautiful Soup
    soup = BeautifulSoup(unescape(str(html_string)), 'html.parser')

    # Remove <img> tags
    for img_tag in soup.find_all('img'):
        img_tag.decompose()

    # Replace <input> tags with a placeholder
    for input_tag in soup.find_all('input'):
        input_tag.replace_with('__________')

    # Remove &nbsp; entities
    for nbsp_tag in soup.find_all(string=lambda t: t == '\xa0'):
        nbsp_tag.string.replace_with('')

    # Get the text content of the modified HTML and return it
    return ' '.join(line.strip() for line in soup.get_text().split() if line.strip())


def insert_newlines(text: str) -> str:
    """
    Inserts a newline after periods and question marks in the input text, unless they are inside parentheses.
    However, does not insert newline if the period is followed by 'i.e.' or 'e.g.'

    :param text: The input string.
    :return: The modified string with newlines inserted.
    """
    result = []
    parenthesis_count = 0

    # Split the text into tokens
    tokens = text.split()

    for i, token in enumerate(tokens):
        if token == '(':
            parenthesis_count += 1
        elif token == ')':
            parenthesis_count -= 1
        elif token.endswith(('.', '!', '?')) and parenthesis_count == 0:
            # Check if the next token is 'i.e.' or 'e.g.'
            next_token = tokens[i + 1] if i + 1 < len(tokens) else ''
            if not next_token.lower() in ['i.e.', 'e.g.']:
                result.append(token)
                result.append('\n')
                continue

        result.append(token)

        if i < len(tokens) - 1:
            # Append a space between tokens
            result.append(' ')

    return ''.join(result)


def extract_points(s: str) -> tuple:
    regex = r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*pts'
    match = re.search(regex, s, re.IGNORECASE)
    if match is None:
        raise ValueError(f'Invalid input string: "{s}"')

    user_points_str, total_points_str = match.groups()
    try:
        user_points = int(user_points_str)
    except ValueError:
        user_points = float(user_points_str)
    try:
        total_points = int(total_points_str)
    except ValueError:
        total_points = float(total_points_str)

    return user_points, total_points


def get_question_text(soup: BeautifulSoup) -> str:
    """
    Extracts the question text from a given div element.

    :param soup: A BeautifulSoup object containing a multiple answer question.
    :return: The question text for the multiple answer question.
    """
    question_textarea = soup.find("textarea", {"name": "question_text"})
    return clean_input(clean_html(question_textarea))


def get_text_from_input(soup: BeautifulSoup, name: str) -> str:
    """
    Extracts the question text from a given div element.

    :param soup: A BeautifulSoup object containing a multiple answer question.
    :param name: The name of the textarea to extract the text from.
    :return: The question text for the multiple answer question.
    """
    question_input = soup.find("input", class_=name)
    answer_text = question_input['value'] if question_input['value'] else NO_ANSWER
    return clean_input(answer_text)


def text_by_filter(soup: BeautifulSoup, initial_filter: str, last_filter: str = None) -> List[str]:
    """
    Retrieves text from the given soup by applying the specified filters.

    :param soup: A BeautifulSoup object
    :param initial_filter: The initial filter to use.
    :param last_filter: The last filter to use, if applicable.
    :return: A list of text elements found after applying the filters.
    """
    if last_filter is None:
        return clean_input([div.get_text() for div in soup.find_all('div', class_=initial_filter)])

    return clean_input([
        div.find("div", class_=last_filter).text if div.find("div", class_=last_filter) else ""
        for div in soup.find_all("div", class_=initial_filter)
    ])


def find_elements_by_class(soup: BeautifulSoup, filter_by: str):
    """
    Find the first element with the specified class.

    :param soup: A BeautifulSoup object.
    :param filter_by: The class to filter the elements by.
    :return: An element with the specified class.
    """
    return soup.find("div", class_=filter_by)


def get_class_names(soup: BeautifulSoup, class_to_search: str) -> list:
    tester_classes = soup.find('div', class_=class_to_search)
    return [name for name in tester_classes.get('class') if name not in ['display_question', 'question']]


def get_title_text(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the title text from a given div element.
    :param soup: A BeautifulSoup object.
    :return: The title text for the quiz.
    """
    title_tag = soup.find('title')

    if title_tag is None:
        return f'No Title Found_{uuid.uuid4()}'

    return "".join(c for c in title_tag.text if c not in (":", ";", ",", '.'))
