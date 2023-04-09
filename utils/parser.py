import logging
from enum import Enum
from typing import Dict
from bs4 import BeautifulSoup

from utils.questions import ShortAnswerQuestion
from utils.utils import clean_input, get_all_questions, extract_points, get_question_text, text_by_filter, \
    find_elements_by_class, get_text_from_input, get_title_text, get_class_names
from utils.quiz import (
    MatchingQuestion,
    MultipleAnswersQuestion,
    MultipleChoiceQuestion,
    MultipleShortAnswerQuestion,
    Quiz)

NO_ANSWER = "CANNOT DETERMINE ANSWER. PLEASE CHECK MANUALLY."


class QuestionTypes(Enum):
    MultipleChoice = 'multiple_choice_question'
    TrueFalse = 'true_false_question'
    MultipleAnswers = 'multiple_answers_question'
    Matching = 'matching_question'
    MultipleShortAnswer = 'fill_in_multiple_blanks_question'
    ShortAnswer = 'short_answer_question'
    Essay = 'essay_question'


# FIXME ERROR HANDLING FOR if user doesnt answer a question
def parse_multiple_choice(soup: BeautifulSoup) -> MultipleChoiceQuestion:
    """
    Processes multiple-choice questions and returns a populated MultipleChoiceQuestion object.

    :return: A MultipleChoiceQuestion object
    """
    mcq = MultipleChoiceQuestion(question=get_question_text(soup),
                                 answer=get_mc_correct_answer(soup),
                                 choices=text_by_filter(soup, "answer", "answer_text"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not mcq.answer and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        mcq.answer = selected_answer[0] if len(selected_answer) > 0 else ""
    elif not mcq.answer and points[0] != points[1]:
        mcq.answer = NO_ANSWER

    return mcq


def parse_multiple_answer(soup: BeautifulSoup) -> MultipleAnswersQuestion:
    """
    Processes multiple-answers questions and returns a populated MultipleAnswersQuestion object.

    :return: A MultipleAnswersQuestion object
    """
    maq = MultipleAnswersQuestion(question=get_question_text(soup),
                                  answers=text_by_filter(soup, "correct_answer", "answer_text"),
                                  choices=text_by_filter(soup, "select_answer"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not maq.answers and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        maq.answers = selected_answer if selected_answer else []
    elif not maq.answers and points[0] != points[1]:
        maq.answers = [NO_ANSWER]

    return maq


def parse_single_matching(soup: BeautifulSoup) -> MatchingQuestion:
    """
    Processes matching questions and returns a list of populated MatchingQuestion objects.

    :return: A MatchingQuestion object.
    """

    mq = MatchingQuestion(question=get_question_text(soup),
                          word_bank=text_by_filter(soup, "answer_match_left"),
                          answer_bank=text_by_filter(soup, "answer_match_right"),
                          answers=None)

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not mq.answers and points[0] == points[1]:
        mq.answers = {k: v for k, v in zip(mq.word_bank, mq.answer_bank)}
    elif not mq.answers and points[0] != points[1]:
        mq.answers = find_matching_answers_dict(soup)

    return mq


def parse_multiple_short_answer(soup) -> MultipleShortAnswerQuestion:
    """
    Processes a multiple short answer question.

    :return: A MultipleShortAnswerQuestion object.
    """

    msa = MultipleShortAnswerQuestion(question=get_question_text(soup),
                                      answers=text_by_filter(soup, "answer_group", "answer_text"))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if not msa.answers and points[0] == points[1]:
        selected_answer = text_by_filter(soup=soup, initial_filter="selected_answer", last_filter="answer_text")
        msa.answers = selected_answer if selected_answer else [NO_ANSWER]

    return msa


def parse_short_answer(soup: BeautifulSoup) -> ShortAnswerQuestion:
    """
    Processes a short answer question.

    :return: A ShortAnswerQuestion object.
    """
    saq = ShortAnswerQuestion(question=get_question_text(soup))

    points = extract_points(find_elements_by_class(soup, 'user_points').get_text(strip=True))

    if points[0] == points[1]:
        selected_answer = get_text_from_input(soup=soup, name="question_input")
        saq.answer = selected_answer if selected_answer else NO_ANSWER
    elif points[0] != points[1]:
        saq.answer = NO_ANSWER

    return saq


def add_to_quiz(quiz: Quiz, question_type: str, soup: BeautifulSoup) -> Quiz:
    """
    Adds a question to the quiz object.

    :param quiz: The quiz object to add the question to.
    :param question_type: The type of question to add.
    :param soup: The soup object containing the question.
    :return: The quiz object with the question added.
    """
    if question_type == QuestionTypes.MultipleChoice.value:
        quiz.multiple_choice_questions.append(parse_multiple_choice(soup))

    elif question_type == QuestionTypes.TrueFalse.value:
        quiz.multiple_choice_questions.append(parse_multiple_choice(soup))

    elif question_type == QuestionTypes.Matching.value:
        quiz.matching_questions.append(parse_single_matching(soup))

    elif question_type == QuestionTypes.MultipleAnswers.value:
        quiz.multiple_answer_questions.append(parse_multiple_answer(soup))

    elif question_type == QuestionTypes.MultipleShortAnswer.value:
        quiz.multiple_short_answer_questions.append(parse_multiple_short_answer(soup))

    elif question_type == QuestionTypes.ShortAnswer.value:
        quiz.short_answer_questions.append(parse_short_answer(soup))

    elif question_type == QuestionTypes.Essay.value:
        logging.info("Essay questions are not supported yet. Skipping.")
    else:
        quiz.unrecognized_questions[question_type].append(soup)
        logging.warning(f"WARNING: Unrecognized question type '{question_type}'")

    return quiz


def process_html(html_content: str) -> Quiz:
    """
    Processes the HTML content and returns a Quiz object.

    :param html_content: The HTML content to process.
    :return: A Quiz object.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    quiz = Quiz(title=get_title_text(soup))

    questions_list = get_all_questions(soup)

    quiz.number_of_questions = len(questions_list)

    for item in questions_list:
        class_names = get_class_names(item, 'display_question')
        question_type = class_names[0] if class_names[0] else "QUESTION TYPE NOT FOUND"

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


def find_matching_answers_dict(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Finds the answers for matching questions.

    :param soup: A BeautifulSoup object.
    :return: A dictionary of answers.
    """
    answers_dict = {}

    wrong_answers = soup.find_all('div', class_='wrong_answer')
    correct_answers = soup.find_all('div', class_=['answer', 'correct_answer'])

    # wrong answers
    if len(wrong_answers) > 0:
        for item in wrong_answers:
            key = item.find("div", class_="answer_match_left").text
            value = item.findNextSibling().find("div", class_="answer_text")
            value = value.get_text(strip=True) if value else NO_ANSWER
            answers_dict[key] = value

    # correct answers
    for item in correct_answers:
        key = item.find("div", class_="answer_match_left")
        value = item.find("div", class_="answer_match_right")
        if key:
            key = key.get_text(strip=True) if key else None
            key = clean_input(key) if key else None
            if key not in answers_dict:
                if value and key:
                    value = clean_input(value.get_text(strip=True))
                    answers_dict[key] = value
            # else:
            #     logging.info(f"Key {key} already exists in answers_dict. Skipping.")
    return answers_dict
