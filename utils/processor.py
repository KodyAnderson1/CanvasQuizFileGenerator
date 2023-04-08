from enum import Enum
from typing import List, Optional

from bs4 import BeautifulSoup

from utils.quiz import MatchingQuestion, MultipleAnswersQuestion, MultipleChoiceQuestion, MultipleShortAnswerQuestion, \
    Quiz
from utils.utils import clean_input, clean_html, get_all_questions, extract_points, remove_tags


class QuestionTypes(Enum):
    MultipleChoice = 'multiple_choice_question'
    TrueFalse = 'true_false_question'
    MultipleAnswers = 'multiple_answers_question'
    Matching = 'matching_question'
    MultipleShortAnswer = 'fill_in_multiple_blanks_question'


# TODO Add error handling if .text is empty

def get_question_text(soup: BeautifulSoup) -> str:
    """
    Extracts the question text from a given div element.

    :param soup: A BeautifulSoup object containing a multiple answer question.
    :return: The question text for the multiple answer question.
    """
    question_textarea = soup.find("textarea", {"name": "question_text"})
    return clean_input(clean_html(question_textarea))


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


def find_all_elements_by_class(soup: BeautifulSoup, filter_by: str):
    """
    Find all elements with the specified class.

    :param soup: A BeautifulSoup object.
    :param filter_by: The class to filter the elements by.
    :return: A list of elements with the specified class.
    """
    return soup.find_all("div", class_=filter_by)


def find_elements_by_class(soup: BeautifulSoup, filter_by: str):
    """
    Find the first element with the specified class.

    :param soup: A BeautifulSoup object.
    :param filter_by: The class to filter the elements by.
    :return: An element with the specified class.
    """
    return soup.find("div", class_=filter_by)


# FIXME ERROR HANDLING FOR if user doesnt answer a question
def process_single_multiple_choice(soup: BeautifulSoup) -> MultipleChoiceQuestion:
    """
    Processes multiple-choice questions and returns a populated MultipleChoiceQuestion object.

    :return: A MultipleChoiceQuestion objects
    """
    mcq = MultipleChoiceQuestion(question=get_question_text(soup),
                                 answer=get_mc_correct_answer(soup),
                                 choices=text_by_filter(soup, "answer", "answer_text"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not mcq.answer and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        mcq.answer = selected_answer[0] if len(selected_answer) > 0 else ""
    elif not mcq.answer and points[0] != points[1]:
        mcq.answer = "CANNOT DETERMINE ANSWER."

    return mcq


def process_single_multiple_answers(soup: BeautifulSoup) -> MultipleAnswersQuestion:
    """
    Extracts multiple answer questions from the HTML source.

    Returns: A list of MultipleAnswersQuestion objects.
    """
    maq = MultipleAnswersQuestion(question=get_question_text(soup),
                                  answers=text_by_filter(soup, "correct_answer", "answer_text"),
                                  choices=text_by_filter(soup, "select_answer"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not maq.answers and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        maq.answers = selected_answer if selected_answer else []
    elif not maq.answers and points[0] != points[1]:
        maq.answers = ["CANNOT DETERMINE ANSWER."]

    return maq


def process_single_matching(soup: BeautifulSoup) -> MatchingQuestion:
    """
    Processes matching questions and returns a list of populated MatchingQuestion objects.

    :return: A list of MatchingQuestion objects.
    """
    matching_question_divs = find_all_elements_by_class(soup, "matching_question")
    # wrong_answers = [div.find_all('div', {'class': 'wrong_answer'}) for div in matching_question_divs]

    mq = MatchingQuestion(question=get_question_text(soup),
                          word_bank=text_by_filter(soup, "answer_match_left"),
                          answer_bank=text_by_filter(soup, "answer_match_right"),
                          # answers=self.get_answers_dict(the_divs, wrong_answer))
                          answers=None)

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not mq.answers and points[0] == points[1]:
        all_choices = text_by_filter(soup=soup, initial_filter="answer_match_left")
        all_options = soup.find_all("div", class_="answer_match_right")
        mq.answers = {k: clean_input(v.get_text(strip=True)) for k, v in zip(all_choices, all_options)}
    elif not mq.answers and points[0] != points[1]:
        mq.answers = {"CANNOT DETERMINE ANSWER": "CANNOT DETERMINE ANSWER"}

    return mq


def process_single_multiple_short_answers(soup) -> MultipleShortAnswerQuestion:
    """
    Processes a multiple short answer question.

    :return: A list containing the question and the answers.
    """

    msa = MultipleShortAnswerQuestion(question=get_question_text(soup),
                                      answers=text_by_filter(soup, "answer_group", "answer_text"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not msa.answers and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        msa.answers = selected_answer if selected_answer else []

    return msa


def add_to_quiz(quiz: Quiz, question_type: str, soup: BeautifulSoup) -> Quiz:
    """

    :param quiz:
    :param question_type:
    :param soup:
    :return:
    """
    if question_type == QuestionTypes.MultipleChoice.value:
        quiz.multiple_choice_questions.append(process_single_multiple_choice(soup))

    elif question_type == QuestionTypes.TrueFalse.value:
        quiz.multiple_choice_questions.append(process_single_multiple_choice(soup))

    elif question_type == QuestionTypes.Matching.value:
        quiz.matching_questions.append(process_single_matching(soup))

    elif question_type == QuestionTypes.MultipleAnswers.value:
        quiz.multiple_answer_questions.append(process_single_multiple_answers(soup))

    elif question_type == QuestionTypes.MultipleShortAnswer.value:
        quiz.multiple_short_answer_questions.append(process_single_multiple_short_answers(soup))
    else:
        quiz.unrecognized_questions[question_type].append(soup)
        print(f"WARNING: Unrecognized question type '{question_type}'")

    return quiz


def get_class_names(soup: BeautifulSoup, class_to_search: str) -> list:
    tester_classes = soup.find('div', class_=class_to_search)
    return [name for name in tester_classes.get('class') if name not in ['display_question', 'question']]


def find_quiz_title(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1", id="quiz_title")
    if not title_tag:
        title_tag = soup.find("header", class_="quiz-header").find("h2")
    return title_tag.text.strip() if title_tag else None


def count_aria_labels(html: str, label_name: str) -> Optional[int]:
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.find_all(attrs={"aria-label": label_name})) if soup else None


def process_html(html_content: str) -> Quiz:
    quiz = Quiz(title=find_quiz_title(html_content), number_of_questions=count_aria_labels(html_content, "Question"))

    soup = remove_tags(html_content)
    questions_list = get_all_questions(soup)

    for item in questions_list:
        class_names = get_class_names(item, 'display_question')
        question_type = class_names[0]  # FIXME. Potential crash if no 0

        add_to_quiz(quiz=quiz, question_type=question_type, soup=item)

    return quiz


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
