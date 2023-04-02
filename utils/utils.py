from html import unescape
from typing import List
import re

from bs4 import BeautifulSoup, Tag


def clean_input(input_obj):
    """
    Cleans an input object by removing extra whitespace, newlines, and empty values.

    :param input_obj: The input object to clean.
    :return: The cleaned object.
    """
    if isinstance(input_obj, str):
        return ' '.join(input_obj.strip().split())
    elif isinstance(input_obj, dict):
        return {k.strip(): v.strip() for k, v in input_obj.items() if v.strip()}
    elif isinstance(input_obj, list):
        return remove_duplicates([' '.join(item.strip().split()) for item in input_obj if item.strip()])
    else:
        return input_obj


def remove_duplicates(input_list) -> List:
    seen = set()
    return [x for x in input_list if not (x in seen or seen.add(x))]


def remove_html_tags(text):
    """
    Removes certain html tags from a string

    :param text: The input string to be cleaned.
    :return: A cleaned string with no html tags.
    """
    pattern = re.compile(r'<[^>]*>|&nbsp;|<img[^>"]+[^>]*')
    clean_text = re.sub(pattern, '', text)
    return clean_text


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
    for nbsp_tag in soup.find_all(text=lambda t: t == '\xa0'):
        nbsp_tag.string.replace_with('')

    # Get the text content of the modified HTML and return it
    return ' '.join(line.strip() for line in soup.get_text().split() if line.strip())


def insert_newlines(text: str) -> str:
    """
    Inserts a newline after periods and question marks in the input text, unless they are inside parentheses.

    :param text: The input string.
    :return: The modified string with newlines inserted.
    """
    result = []
    parenthesis_count = 0

    for char in text:
        if char == '(':
            parenthesis_count += 1
        elif char == ')':
            parenthesis_count -= 1
        elif char in '.!?' and parenthesis_count == 0:
            result.append(char)
            result.append('\n')
            continue

        result.append(char)

    return ''.join(result)
