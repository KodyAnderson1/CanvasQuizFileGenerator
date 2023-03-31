from typing import Dict, List
import re


def clean_dict(dictionary: Dict[str, str]) -> Dict[str, str]:
    """
    Removes all but one whitespace between words, removes newlines, and removes keys with empty values.

    :param dictionary: The input dictionary to be cleaned.
    :return: A cleaned dictionary with no extra whitespaces or newline characters and no keys with empty values.
    """
    cleaned_dict = {k.strip(): v.strip() for k, v in dictionary.items() if v.strip()}
    return cleaned_dict


def clean_list(lst: List[str]) -> List[str]:
    """
    Removes all but one whitespace between words, removes newlines from a list, and removes duplicate items.

    :param lst: The input list to be cleaned.
    :return: A cleaned list with no extra whitespaces, newline characters, or duplicate items.
    """
    cleaned_lst = [' '.join(item.strip().split()) for item in lst]
    cleaned_lst = list(set(cleaned_lst))
    return [item for item in cleaned_lst if item]


def clean_string(s: str) -> str:
    """
    Removes all but one whitespace between words and removes newlines from a string.

    :param s: The input string to be cleaned.
    :return: A cleaned string with no extra whitespaces or newline characters.
    """
    s = ' '.join(s.strip().split())
    return s


def remove_html_tags(text):
    """
    Removes certain html tags from a string

    :param text: The input string to be cleaned.
    :return: A cleaned string with no html tags.
    """
    pattern = re.compile(r'<[^>]*>|&nbsp;|<img[^>"]+[^>]*')
    clean_text = re.sub(pattern, '', text)
    return clean_text
