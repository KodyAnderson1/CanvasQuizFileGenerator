from collections import defaultdict
from typing import List

from utils.questions import (
    MultipleShortAnswerQuestion,
    MultipleChoiceQuestion,
    MultipleAnswersQuestion,
    MatchingQuestion,
)


class Quiz:
    """
    A class representing a quiz with multiple choice and matching questions.

    :param title: The title of the quiz
    :param number_of_questions: The total number of questions in the quiz
    """

    def __init__(self, title: str = "", number_of_questions: int = 0):
        self.title: str = title
        self.number_of_questions = number_of_questions
        self.multiple_choice_questions: List[MultipleChoiceQuestion] = []
        self.matching_questions: List[MatchingQuestion] = []
        self.multiple_answer_questions: List[MultipleAnswersQuestion] = []
        self.multiple_short_answer_questions: List[MultipleShortAnswerQuestion] = []
        self.unrecognized_questions: dict = defaultdict(list)

    def __repr__(self):
        return f"Title = {self.title}\nNumber_of_questions = {self.number_of_questions} " \
               f"\nMultiple_choice_questions =\n{self.multiple_choice_questions} " \
               f"\nMatching questions =\n{self.matching_questions}" \
               f"\nMultiple_answer_questions =\n{self.multiple_answer_questions}" \
               f"\nmultiple_short_answer_questions =\n{self.multiple_short_answer_questions}"

    def to_dict(self):
        return {
            "title": self.title,
            "number_of_questions": self.number_of_questions,
            "multiple_choice_questions": [mcq.__dict__ for mcq in self.multiple_choice_questions],
            "matching_questions": [mq.__dict__ for mq in self.matching_questions],
            "multiple_answers_questions": [maq.__dict__ for maq in self.multiple_answer_questions],
            "multiple_short_answer_questions": [msaq.__dict__ for msaq in self.multiple_short_answer_questions]
        }
