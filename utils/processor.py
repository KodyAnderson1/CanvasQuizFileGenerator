from typing import List, Dict
from bs4 import BeautifulSoup, Tag

from utils.quiz import MatchingQuestion, MultipleAnswersQuestion, MultipleChoiceQuestion, MultipleShortAnswerQuestion
from utils.utils import clean_input, remove_html_tags, clean_html


# TODO Add error handling if .text is empty

def get_question_text(soup: BeautifulSoup) -> str:
    """
    Extracts the question text from a given div element.

    :param soup: A BeautifulSoup object containing a multiple answer question.
    :return: The question text for the multiple answer question.
    """
    question_textarea = soup.find("textarea", {"name": "question_text"})
    return remove_html_tags(clean_input(clean_html(question_textarea)))


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
    Find all elements with the specified class.

    :param soup: A BeautifulSoup object.
    :param filter_by: The class to filter the elements by.
    :return: A list of elements with the specified class.
    """
    return soup.find_all("div", class_=filter_by)


class ProcessQuestions:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def process_multiple_answers(self) -> List[MultipleAnswersQuestion]:
        """
        Extracts multiple answer questions from the HTML source.

        Returns: A list of MultipleAnswersQuestion objects.
        """
        return [MultipleAnswersQuestion(question=get_question_text(div),
                                        answers=text_by_filter(div, "correct_answer", "answer_text"),
                                        choices=text_by_filter(div, "select_answer"))
                for div in find_elements_by_class(self.soup, "multiple_answers_question")]

    def process_multiple_choice(self) -> List[MultipleChoiceQuestion]:
        """
        Processes multiple-choice questions and returns a list of populated MultipleChoiceQuestion objects.

        :return: A list of MultipleChoiceQuestion objects.
        """
        return [MultipleChoiceQuestion(question=get_question_text(div),
                                       answer=self.get_mc_correct_answer(div),
                                       choices=text_by_filter(div, "answer", "answer_text"))
                for div in find_elements_by_class(self.soup, "multiple_choice_question")]

    def process_matching(self) -> List[MatchingQuestion]:
        """
        Processes matching questions and returns a list of populated MatchingQuestion objects.

        :return: A list of MatchingQuestion objects.
        """
        matching_question_divs = find_elements_by_class(self.soup, "matching_question")
        wrong_answers = [div.find_all('div', {'class': 'wrong_answer'}) for div in matching_question_divs]

        return [MatchingQuestion(question=get_question_text(the_divs),
                                 word_bank=text_by_filter(the_divs, "answer_match_left"),
                                 answer_bank=text_by_filter(the_divs, "answer_match_right"),
                                 answers=self.get_answers_dict(the_divs, wrong_answer))
                for the_divs, wrong_answer in zip(matching_question_divs, wrong_answers)]

    def process_multiple_short_answers(self) -> list[MultipleShortAnswerQuestion]:
        """
        Processes a multiple short answer question.

        :return: A list containing the question and the answers.
        """
        return [MultipleShortAnswerQuestion(question=get_question_text(div),
                                            answers=text_by_filter(div, "answer_group", "answer_text"))
                for div in find_elements_by_class(self.soup, "fill_in_multiple_blanks_question")]

    @staticmethod
    def get_mc_correct_answer(soup: BeautifulSoup) -> str:
        """
        Retrieves the correct answer from a multiple-choice question element.

        :param soup: A BeautifulSoup object representing a multiple-choice question element.
        :return: The correct answer as a string.
        """
        correct_answer_div = soup.find("div", class_="correct_answer")
        answer_text_div = correct_answer_div.find("div", class_="answer_text") if correct_answer_div else None

        if not answer_text_div:
            intermediate_div = soup.find("div", class_="answer_for_correct_answer")
            answer_text_div = intermediate_div.find("div", class_="answer_text") if intermediate_div else None

        return clean_input(answer_text_div.text) if answer_text_div else ""

    def get_answers_dict(self, the_divs, wrong_answer) -> dict:
        """
        Retrieves the matching answers from a matching question element.

        :param the_divs: A BeautifulSoup object representing a matching question element.
        :param wrong_answer: A list of wrong answers (divs).
        :return: A dictionary of matching answers.
        """
        answer_divs = [div for div in the_divs.find_all('div', {'class': 'answer'}) if div.has_attr('id')]
        full_dict = {k: v for each_div in answer_divs for k, v in self.get_matching_answers(each_div).items()}

        wrong_answer_dict = {stuff.get('title').split("You selected", 1)[0].strip().replace(".", ""):
                                 stuff.get('title').split("The correct answer was", 1)[1].strip().replace(".", "")
                             for stuff in wrong_answer}
        full_dict.update(wrong_answer_dict)

        return clean_input(full_dict)

    @staticmethod
    def get_matching_answers(parent_div: Tag) -> Dict[str, str]:
        """
        Retrieves the matching answers from a matching question element.

        :param parent_div: A BeautifulSoup object representing a matching question element.
        :return: A dictionary of matching answers.
        """
        is_correct = 'wrong_answer' not in parent_div.get('class')

        matching_answers_dict = {}
        matching_answer_divs = parent_div.find_all('div', {'class': 'matching_answer'})

        for matching_answer_div in matching_answer_divs:
            answer_match_left_div = matching_answer_div.find('div', {'class': 'answer_match_left'})
            if answer_match_left_div:
                key = answer_match_left_div.get_text(strip=True).strip().replace("\n", "")
                key = " ".join(key.split())
                option = matching_answer_div.find('option')
                if option and is_correct:
                    value = option.get_text(strip=True).strip().replace("\n", "")
                    matching_answers_dict[key] = " ".join(value.split())

        return matching_answers_dict
