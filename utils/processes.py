from typing import List, Dict

from bs4 import BeautifulSoup, Tag

from utils.quiz import MatchingQuestion, MultipleAnswersQuestion, MultipleChoiceQuestion
from utils.utils import clean_dict, clean_list, clean_string, remove_html_tags


class ProcessMultipleAnswers:
    """
    A class to process multiple answer questions from an HTML source.

    :ivar soup: A BeautifulSoup object containing the HTML source.
    """

    def __init__(self, soup: BeautifulSoup = None):
        self.soup = soup

    def process(self) -> List[MultipleAnswersQuestion]:
        """
        Extracts multiple answer questions from the HTML source.

        Returns: A list of MultipleAnswersQuestion objects.
        """
        multiple_answers_questions = []
        for div in self.find_all_multiple_answers_questions():
            maq = MultipleAnswersQuestion(question=self.get_question_text(div),
                                          answers=self.get_correct_choices_for_question(div),
                                          choices=self.get_all_choices_for_question(div))

            multiple_answers_questions.append(maq)
        return multiple_answers_questions

    def find_all_multiple_answers_questions(self) -> List[BeautifulSoup]:
        """
        Finds all div elements with multiple answer questions in the HTML source.

        Returns: A list of BeautifulSoup objects containing multiple answer questions.
        """
        return self.soup.find_all("div", class_="multiple_answers_question")

    @staticmethod
    def get_question_text(soup: BeautifulSoup) -> str:
        """
        Extracts the question text from a given div element.

        :param soup: A BeautifulSoup object containing a multiple answer question.
        :return: The question text for the multiple answer question.
        """
        question_textarea = soup.find("textarea", {"name": "question_text"})
        return remove_html_tags(clean_string(question_textarea.text.strip("<p></p>")))

    @staticmethod
    def get_all_choices_for_question(soup: BeautifulSoup) -> List[str]:
        """
        Extracts all choices for a multiple answer question from a given div element.

        :param soup: A BeautifulSoup object containing a multiple answer question.
        :return: A list of choices for the multiple answer question.
        """
        return clean_list([div.get_text() for div in soup.find_all("div", class_="select_answer")])

    @staticmethod
    def get_correct_choices_for_question(soup: BeautifulSoup) -> List[str]:
        """
        Extracts the correct choices for a multiple answer question from a given div element.

        :param: A BeautifulSoup object containing a multiple answer question.
        :return: A list of correct choices for the multiple answer question.
        """
        init_list = [div for div in soup.find_all("div", class_="correct_answer")]
        return clean_list([div.find("div", class_="answer_text").get_text(strip=True) for div in init_list])


class ProcessMultipleChoice:
    """
    A class to process multiple choice questions from an HTML source.

    :ivar soup: A BeautifulSoup object containing the HTML source.
    """

    def __init__(self, soup: BeautifulSoup = None):
        self.soup = soup

    def process(self) -> List[MultipleChoiceQuestion]:
        """
        Processes multiple-choice questions and returns a list of populated MultipleChoiceQuestion objects.

        :return: A list of MultipleChoiceQuestion objects.
        """
        multiple_choice_questions = []

        for div in self.find_multiple_choice_questions():
            mcq = MultipleChoiceQuestion()
            mcq.question = remove_html_tags(self.get_question_text(div))
            mcq.choices = clean_list(self.get_choices_text_mcq(div))
            mcq.answer = clean_string(self.get_correct_answer(div))

            multiple_choice_questions.append(mcq)

        return multiple_choice_questions

    def find_multiple_choice_questions(self) -> List[BeautifulSoup]:
        """
        Finds all the multiple-choice question elements in the BeautifulSoup object.

        :return: A list of multiple-choice question elements.
        """
        return self.soup.find_all("div", class_="multiple_choice_question")

    @staticmethod
    def get_question_text(soup: BeautifulSoup) -> str:
        """
        Retrieves the question text from a multiple-choice question element.

        :param soup: A BeautifulSoup object representing a multiple-choice question element.
        :return: The question text as a string.
        """
        question_textarea = soup.find("textarea", {"name": "question_text"})
        return question_textarea.text.strip("<p></p>")

    @staticmethod
    def get_correct_answer(soup: BeautifulSoup) -> str:
        """
        Retrieves the correct answer from a multiple-choice question element.

        :param soup: A BeautifulSoup object representing a multiple-choice question element.
        :return: The correct answer as a string.
        """
        correct_answer_div = soup.find("div", class_="correct_answer")
        answer_text_div = correct_answer_div.find("div", class_="answer_text") if correct_answer_div else None
        return answer_text_div.text.strip() if answer_text_div else ""

    @staticmethod
    def get_choices_text_mcq(soup: BeautifulSoup) -> List[str]:
        """
        Retrieves the choices text from a multiple-choice question element.

        :param soup: A BeautifulSoup object representing a multiple-choice question element.
        :return: A list of choices text.
        """
        answer_wrapper_divs = soup.find_all("div", class_="answers_wrapper")
        return [answer_text_div.text.strip() for answer_wrapper_div in answer_wrapper_divs for answer_div in
                answer_wrapper_div.find_all("div", class_="answer") if
                (answer_text_div := answer_div.find("div", class_="answer_text")) is not None]


class ProcessMatchingQuestions:
    """
    Processes matching questions and returns a list of populated MatchingQuestion objects.

    :ivar soup: A BeautifulSoup object containing the HTML source.
    """

    def __init__(self, soup: BeautifulSoup = None):
        self.soup = soup

    def process(self) -> List[MatchingQuestion]:
        """
        Processes matching questions and returns a list of populated MatchingQuestion objects.

        :param soup: A BeautifulSoup object containing the HTML source.
        :return: A list of MatchingQuestion objects.
        """
        return_list = []
        all_questions = self.get_questions(self.soup)
        all_matching_questions = self.find_matching_questions(all_questions)
        wrong_answers = [div.find_all('div', {'class': 'wrong_answer'}) for div in all_matching_questions]

        for the_divs in all_matching_questions:
            matching_question = MatchingQuestion()
            matching_question.word_bank = self.get_matching_words(the_divs)
            matching_question.answer_bank = self.get_matching_choices(the_divs)

            textarea = the_divs.find('textarea', {'class': 'textarea_question_text'})
            matching_question.question = remove_html_tags(clean_string(textarea.text.strip())) if textarea else ""

            answer_divs = [div for div in the_divs.find_all('div', {'class': 'answer'}) if div.has_attr('id')]
            full_dict = {}
            for each_div in answer_divs:
                full_dict.update(self.get_matching_answers(each_div))

            for wrong_answer in wrong_answers:
                for stuff in wrong_answer:
                    here = stuff.get('title')
                    key = here.split("You selected", 1)[0].strip().replace(".", "")
                    value = here.split("The correct answer was", 1)[1].strip().replace(".", "")
                    full_dict[key] = value

            matching_question.answers = full_dict

            matching_question.answers = clean_dict(matching_question.answers)
            matching_question.answer_bank = clean_list(matching_question.answer_bank)
            matching_question.word_bank = clean_list(matching_question.word_bank)
            return_list.append(matching_question)

        return return_list

    @staticmethod
    def get_matching_words(soup: BeautifulSoup) -> List[str]:
        """
        Retrieves the matching words from a matching question element.
        :param soup: A BeautifulSoup object representing a matching question element.
        :return: A list of matching words.
        """
        return [div.get_text(strip=True) for div in soup.find_all('div', {'class': 'answer_match_left'})]

    @staticmethod
    def get_matching_choices(soup: BeautifulSoup) -> List[str]:
        """
        Retrieves the matching choices from a matching question element.

        :param soup: A BeautifulSoup object representing a matching question element.
        :return: A list of matching choices.
        """
        return [div.get_text(strip=True) for div in soup.find_all('div', {'class': 'answer_match_right'})]

    @staticmethod
    def get_questions(soup: BeautifulSoup) -> List:
        """
        Retrieves all the questions from a BeautifulSoup object.

        :param soup: A BeautifulSoup object containing the HTML source.
        :return: A list of question elements.
        """
        return soup.find_all('div', {'aria-label': 'Question'})

    @staticmethod
    def find_matching_questions(divs: List) -> List:
        """
        Finds all the matching questions in a list of question elements.
        :param divs: A list of question elements.
        :return: A list of matching question elements.
        """
        return [div.find('div', {'class': 'matching_question'}) for div in divs if
                div.find('div', {'class': 'matching_question'})]

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
