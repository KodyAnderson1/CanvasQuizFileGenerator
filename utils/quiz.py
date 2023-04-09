from collections import defaultdict
from typing import List, Dict, Any

from utils.questions import (
    MultipleShortAnswerQuestion,
    MultipleChoiceQuestion,
    MultipleAnswersQuestion,
    MatchingQuestion, ShortAnswerQuestion,
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
        self.short_answer_questions: List[ShortAnswerQuestion] = []
        self.unrecognized_questions: dict = defaultdict(list)

    def __repr__(self):
        return f"Title = {self.title}\nNumber_of_questions = {self.number_of_questions} " \
               f"\nMultiple_choice_questions =\n{self.multiple_choice_questions} " \
               f"\nMatching questions =\n{self.matching_questions}" \
               f"\nMultiple_answer_questions =\n{self.multiple_answer_questions}" \
               f"\nmultiple_short_answer_questions =\n{self.multiple_short_answer_questions} " \
               f"\nshort_answer_questions =\n{self.short_answer_questions} "

    def to_dict(self):
        return {
            "title": self.title,
            "number_of_questions": self.number_of_questions,
            "multiple_choice_questions": [mcq.__dict__ for mcq in self.multiple_choice_questions],
            "matching_questions": [mq.__dict__ for mq in self.matching_questions],
            "multiple_answers_questions": [maq.__dict__ for maq in self.multiple_answer_questions],
            "multiple_short_answer_questions": [msaq.__dict__ for msaq in self.multiple_short_answer_questions],
            "short_answer_questions": [saq.__dict__ for saq in self.short_answer_questions],
        }

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'Quiz':
        quiz = Quiz(title=json_data["title"], number_of_questions=json_data["number_of_questions"])

        for mcq_data in json_data["multiple_choice_questions"]:
            mcq = MultipleChoiceQuestion(question=mcq_data["question"], answer=mcq_data["answer"],
                                         choices=mcq_data["choices"])
            quiz.multiple_choice_questions.append(mcq)

        for maq_data in json_data["multiple_answers_questions"]:
            maq = MultipleAnswersQuestion(question=maq_data["question"], answers=maq_data["answers"],
                                          choices=maq_data["choices"])
            quiz.multiple_answer_questions.append(maq)

        for msaq_data in json_data["multiple_short_answer_questions"]:
            msaq = MultipleShortAnswerQuestion(question=msaq_data["question"], answers=msaq_data["answers"])
            quiz.multiple_short_answer_questions.append(msaq)

        for saq_data in json_data["short_answer_questions"]:
            saq = ShortAnswerQuestion(question=saq_data["question"], answer=saq_data["answer"])
            quiz.short_answer_questions.append(saq)

        for mq_data in json_data["matching_questions"]:
            mq = MatchingQuestion(
                question=mq_data["question"],
                answers=mq_data["answers"],
                answer_bank=mq_data["answer_bank"],
                word_bank=mq_data["word_bank"],
            )
            quiz.matching_questions.append(mq)

        return quiz

    # The code for the json_to_quiz function goes here

    def combine(self, other: 'Quiz') -> 'Quiz':
        combined_quiz = Quiz(
            title=self.title + " & " + other.title,
            number_of_questions=self.number_of_questions + other.number_of_questions
        )

        seen_questions = set()

        for question in self.multiple_choice_questions + other.multiple_choice_questions:
            if question not in seen_questions:
                seen_questions.add(question)
                combined_quiz.multiple_choice_questions.append(question)

        seen_questions.clear()

        for question in self.multiple_answer_questions + other.multiple_answer_questions:
            if question not in seen_questions:
                seen_questions.add(question)
                combined_quiz.multiple_answer_questions.append(question)

        seen_questions.clear()

        for question in self.multiple_short_answer_questions + other.multiple_short_answer_questions:
            if question not in seen_questions:
                seen_questions.add(question)
                combined_quiz.multiple_short_answer_questions.append(question)

        seen_questions.clear()

        for question in self.short_answer_questions + other.short_answer_questions:
            if question not in seen_questions:
                seen_questions.add(question)
                combined_quiz.short_answer_questions.append(question)

        seen_questions.clear()

        for question in self.matching_questions + other.matching_questions:
            if question not in seen_questions:
                seen_questions.add(question)
                combined_quiz.matching_questions.append(question)

        return combined_quiz


