from typing import Dict, List
import re


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
        return list(set([' '.join(item.strip().split()) for item in input_obj if item.strip()]))
    else:
        return input_obj


def remove_html_tags(text):
    """
    Removes certain html tags from a string

    :param text: The input string to be cleaned.
    :return: A cleaned string with no html tags.
    """
    pattern = re.compile(r'<[^>]*>|&nbsp;|<img[^>"]+[^>]*')
    clean_text = re.sub(pattern, '', text)
    return clean_text


def clean_html(soup) -> str:
    """
    Cleans an HTML string by removing img tags, replacing input tags with a placeholder, and removing &nbsp; entities.

    :param soup: The HTML string to clean.
    :return: The cleaned HTML string.
    """

    for img_tag in soup.find_all('img'):
        img_tag.decompose()

    for input_tag in soup.find_all('input'):
        input_tag.replace_with('__________')

    for nbsp_tag in soup.find_all(text=lambda t: t == '\xa0'):
        nbsp_tag.string.replace_with('')

    return '\n\n'.join(line.strip() for line in soup.get_text().split('\n') if line.strip())
