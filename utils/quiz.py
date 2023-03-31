from pathlib import Path
from typing import List, Union, Dict
import toml
import json
import yaml

from utils.utils import remove_html_tags

INITAL_HEADING = f"==========================================\n             QUIZ INFORMATION\n==========================================\n"
MULTIPLE_CHOICE_HEADING = f"==========================================\n         MULTIPLE CHOICE QUESTIONS\n==========================================\n"
MULTIPLE_ANSWERS_HEADING = f"==========================================\n        MULTIPLE ANSWER QUESTIONS\n==========================================\n"
MATCHING_QUESTIONS_HEADING = f"==========================================\n             MATCHING QUESTIONS\n==========================================\n"
DASHES_WITH_NEWLINES = "\n--------------------------------\n\n"


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

    def __repr__(self):
        return f"Title = {self.title}\nNumber_of_questions = {self.number_of_questions} " \
               f"\nMultiple_choice_questions =\n{self.multiple_choice_questions} " \
               f"\nMatching questions =\n{self.matching_questions}" \
               f"\nMultiple_answer_questions =\n{self.multiple_answer_questions}"

    def to_dict(self):
        return {
            "title": self.title,
            "number_of_questions": self.number_of_questions,
            "multiple_choice_questions": [mcq.__dict__ for mcq in self.multiple_choice_questions],
            "matching_questions": [mq.__dict__ for mq in self.matching_questions],
            "multiple_answers_questions": [maq.__dict__ for maq in self.multiple_answer_questions]
        }

    def write_text_file(self, file_name: str):
        """
        Write the Quiz object to a text file with the specified file name.

        :param file_name: The name of the text file to write.
        """
        with open(file_name, 'w', encoding='utf-8') as text_file:

            text_file.write(INITAL_HEADING)
            text_file.write(f"Title: {self.title}\n\nNumber of questions: {self.number_of_questions}\n")
            if len(self.multiple_choice_questions) > 0:
                text_file.write(f"Number of multiple choice questions: {len(self.multiple_choice_questions)}\n")
            if len(self.matching_questions) > 0:
                text_file.write(f"Number of matching questions: {len(self.matching_questions)}\n")
            if len(self.multiple_answer_questions) > 0:
                text_file.write(f"Number of multiple answers questions: {len(self.multiple_answer_questions)}\n")

            if len(self.multiple_choice_questions) > 0:
                text_file.write(MULTIPLE_CHOICE_HEADING)

            for mcq in self.multiple_choice_questions:
                question = remove_html_tags(mcq.question)
                choices = "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(mcq.choices)])
                answer = mcq.answer

                text_file.write(f"{question}\n"
                                f"{choices}\n\nAnswer: {answer}{DASHES_WITH_NEWLINES}")

            if len(self.matching_questions) > 0:
                text_file.write(MULTIPLE_ANSWERS_HEADING)

            for maq in self.multiple_answer_questions:
                question = maq.question
                choices = "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(maq.choices)])
                answers = ", ".join(maq.answers)

                text_file.write(f"{question}\n{choices}\n\nAnswer(s): {answers}{DASHES_WITH_NEWLINES}")

            if len(self.multiple_answer_questions) > 0:
                text_file.write(MATCHING_QUESTIONS_HEADING)

            for mq in self.matching_questions:
                question = mq.question
                answer_bank = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(mq.answer_bank)])
                word_bank = "\n".join([f"{i + 1}. {word}" for i, word in enumerate(mq.word_bank)])
                answers = "\n".join([f"{key} : {value}" for key, value in mq.answers.items()])

                text_file.write(f"{question}\n\nAnswer Bank:\n{answer_bank}\n\n"
                                f"Word Bank:\n{word_bank}\n\nAnswers:\n{answers}{DASHES_WITH_NEWLINES}")

    def write_toml_file(self, file_name: str):
        """
        Write the Quiz object to a TOML file with the specified file name.

        :param file_name: The name of the TOML file to write.
        """

        with open(file_name, 'w') as toml_file:
            toml_file.write(toml.dumps(self.to_dict()))

    def write_yaml_file(self, file_name: str):
        """
        Write the Quiz object to a YAML file with the specified file name.

        :param file_name: The name of the YAML file to write.
        """
        with open(file_name, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(self.to_dict(), yaml_file, default_flow_style=False, allow_unicode=True)

    def write_json_file(self, file_name: str):
        """
        Write the Quiz object to a JSON file with the specified file name.

        :param file_name: The name of the JSON file to write.
        """
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.to_dict(), json_file, ensure_ascii=False, indent=4)


class MultipleAnswersQuestion:
    """
    A class representing a multiple-answers question.

    :param question: The text of the question
    :param answers: A list of correct answers to the question
    :param choices: A list of choices for the question
    """

    def __init__(self, question: str = "", answers: List[str] = [], choices: List[str] = []):
        self.question: str = question
        self.answers: List[str] = answers
        self.choices: List[str] = choices

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswers =\n{self.answers}\nChoices =\n{self.choices}\n"


class MultipleChoiceQuestion:
    """
     A class representing a multiple-choice question.

     :param question: The text of the question
     :param answer: The correct answer to the question
     :param choices: A list of choices for the question
     """

    def __init__(self, question: str = "", answer: str = "", choices: List[str] = None):
        self.question = question
        self.answer = answer
        self.choices = choices if choices else []

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswer = {self.answer}\nChoices = {self.choices}\n"


class MatchingQuestion:
    """
    A class representing a matching question.

    :param question: The text of the question
    :param answers: A dictionary containing the correct matches
    :param answer_bank: A list of answers to be matched
    :param word_bank: A list of words to be matched with the answers
    """

    def __init__(
            self,
            question: str = "Placeholder question",
            answers: Dict[str, str] = {},
            answer_bank: List[str] = [],
            word_bank: List[str] = [],
    ):
        self.question = question
        self.answers = answers
        self.answer_bank = answer_bank
        self.word_bank = word_bank

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswers = {self.answers}" \
               f"\nAnswer bank = {self.answer_bank}\nWord bank = {self.word_bank}\n"


class QuizFileGenerator:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def save_quiz_as_file(self, file_types: Union[List[str], str], output_file: Path) -> None:
        if isinstance(file_types, str):
            file_types = [file_types]

        file_writers = {
            "txt": self.quiz.write_text_file,
            "json": self.quiz.write_json_file,
            "yaml": self.quiz.write_yaml_file,
            "toml": self.quiz.write_toml_file,
        }

        for file_type in file_types:
            writer = file_writers.get(file_type)
            if writer:
                output_file_with_ext = output_file.with_suffix(f".{file_type}")
                writer(output_file_with_ext)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
