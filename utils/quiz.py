from pathlib import Path
from typing import List, Union
import toml
import json
import yaml

from utils.question_classes import (
    MultipleShortAnswerQuestion,
    MultipleChoiceQuestion,
    MultipleAnswersQuestion,
    MatchingQuestion,
)

BETA_MESSAGE = " **This section is still in beta. Please report any bugs.**"
BETA_CLASSES = [MultipleAnswersQuestion, MultipleShortAnswerQuestion, MatchingQuestion, MultipleChoiceQuestion]

HEADINGS = {
    "initial": ("=" * 42) + "\n" + (" " * 13) + "QUIZ INFORMATION\n" + ("=" * 42) + "\n",
    "multiple_choice": ("=" * 42) + "\n" + (" " * 9) + "MULTIPLE CHOICE QUESTIONS\n" + ("=" * 42) + "\n\n",
    "multiple_answers": ("=" * 42) + "\n" + (" " * 9) + "MULTIPLE ANSWER QUESTIONS\n" + ("=" * 42) + "\n\n",
    "matching": ("=" * 42) + "\n" + (" " * 14) + "MATCHING QUESTIONS\n" + ("=" * 42) + "\n\n",
    "multiple_short_answers": ("=" * 42) + "\n" + (" " * 6) + "MULTIPLE SHORT ANSWER QUESTIONS\n" + ("=" * 42) + "\n\n",
}

DASHES_WITH_NEWLINES = f"\n{'-' * 32}\n\n"
NEWLINE = "\n"


def write_question_summary(questions: list, heading_text: str) -> str:
    beta_message = (
        f"{BETA_MESSAGE}"
        if any(isinstance(q, cls) for q in questions for cls in BETA_CLASSES)
        else ""
    )
    return f"Number of {heading_text}: {len(questions)}{beta_message}\n"


def write_markdown_summary(questions: list, heading: str, count: int) -> str:
    beta_message = (
        f"{BETA_MESSAGE}"
        if any(isinstance(q, cls) for q in questions for cls in BETA_CLASSES)
        else ""
    )
    return f"- Number of [{heading}](#{heading.lower().replace(' ', '-')}): {count}{beta_message}\n"


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


class QuizWriter:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def write(self, file_types: Union[List[str], str], output_file: Path) -> None:
        if isinstance(file_types, str):
            file_types = [file_types]

        file_writers = {
            "txt": self.write_text_file,
            "json": self.write_json_file,
            "yaml": self.write_yaml_file,
            "md": self.write_markdown_file,
        }

        for file_type in file_types:
            writer = file_writers.get(file_type)
            if writer:
                output_file_with_ext = output_file.with_suffix(f".{file_type}")
                writer(output_file_with_ext)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

    def write_text_file(self, file_name: str):
        """
        Write the Quiz object to a text file with the specified file name.

        :param file_name: The name of the text file to write.
        """

        with open(file_name, 'w', encoding='utf-8') as text_file:

            mcq, mq = self.quiz.multiple_choice_questions, self.quiz.matching_questions
            maq, msaq = self.quiz.multiple_answer_questions, self.quiz.multiple_short_answer_questions
            sections = [
                (len(mcq), HEADINGS["multiple_choice"], "multiple choice questions", mcq),
                (len(mq), HEADINGS["matching"], "matching questions", mq),
                (len(maq), HEADINGS["multiple_answers"], "multiple answers questions", maq),
                (len(msaq), HEADINGS["multiple_short_answers"], "multiple short answer questions", msaq)
            ]

            text_file.write(HEADINGS["initial"])
            text_file.write(f"Title: {self.quiz.title}\n\nNumber of questions: {self.quiz.number_of_questions}\n")

            for count, heading, heading_text, questions in sections:
                if count > 0:
                    text_file.write(write_question_summary(questions, heading_text))

            for count, heading, heading_text, questions in sections:
                if count > 0:
                    text_file.write(heading)
                    for q in questions:
                        question = q.question

                        if isinstance(q, MatchingQuestion):
                            answer_bank = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(q.answer_bank)])
                            word_bank = "\n".join([f"{i + 1}. {word}" for i, word in enumerate(q.word_bank)])
                            choices = f"Answer Bank:\n{answer_bank}\n\nWord Bank:\n{word_bank}\n"
                            answer = f"Answers:\n{f'{NEWLINE}'.join([f'{key} : {value}' for key, value in q.answers.items()])}"
                        elif isinstance(q, MultipleShortAnswerQuestion):
                            choices = ""
                            answer = f"Answer(s): {f', '.join(q.answers)}"
                        else:
                            choices = "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(q.choices)])
                            if isinstance(q, MultipleChoiceQuestion):
                                answer = f"Answer: {q.answer}"
                            elif isinstance(q, MultipleAnswersQuestion):
                                answer = f"Answer(s): \n{f'{NEWLINE}'.join(q.answers)}"

                        text_file.writelines([f"{question}\n{choices}\n\n{answer}{DASHES_WITH_NEWLINES}"])

    def write_markdown_file(self, file_name: str):
        """
        Write the Quiz object to a markdown file with the specified file name.

        :param file_name: The name of the text file to write.
        """
        dashes = f"\n\n{'-' * 3}\n\n"
        answ_heading = "#### _Answer(s):_"

        with open(file_name, 'w', encoding='utf-8') as text_file:

            mcq, mq = self.quiz.multiple_choice_questions, self.quiz.matching_questions
            maq, msaq = self.quiz.multiple_answer_questions, self.quiz.multiple_short_answer_questions
            sections = [
                (len(mcq), "Multiple Choice Questions", mcq),
                (len(mq), "Matching Questions", mq),
                (len(maq), "Multiple Answer Questions", maq),
                (len(msaq), "Multiple Short Answer Questions", msaq)
            ]

            text_file.write(f"# {self.quiz.title}\n\n- Number of questions: {self.quiz.number_of_questions}\n")

            for count, heading, questions in sections:
                if count > 0:
                    text_file.write(write_markdown_summary(questions, heading, count))

            text_file.write(f"\n{dashes}\n")

            for count, heading, questions in sections:
                if count > 0:
                    text_file.write(f"## {heading}\n")
                    for q in questions:
                        question = f"#### {q.question}"

                        if isinstance(q, MatchingQuestion):
                            answer_bank = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(q.answer_bank)])
                            word_bank = "\n".join([f"{i + 1}. {word}" for i, word in enumerate(q.word_bank)])
                            choices = f"#### Answer Bank:\n{answer_bank}\n\n#### Word Bank:\n{word_bank}\n"
                            answer = f"{answ_heading}{''.join([f' {NEWLINE}- {key} : {value}' for key, value in q.answers.items()])}"
                        elif isinstance(q, MultipleShortAnswerQuestion):
                            choices = f"{BETA_MESSAGE}"
                            answer = f"{answ_heading} {f', '.join(q.answers)}"
                        else:
                            choices = "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(q.choices)])
                            if isinstance(q, MultipleChoiceQuestion):
                                answer = f"{answ_heading} {q.answer}"
                            elif isinstance(q, MultipleAnswersQuestion):
                                answer = f'{answ_heading}{f"".join([f"{NEWLINE}- {choice}" for choice in q.answers])}'

                        text_file.writelines([f"{question}\n{choices}\n\n{answer}{dashes}"])

    def write_yaml_file(self, file_name: str):
        """
        Write the Quiz object to a YAML file with the specified file name.

        :param file_name: The name of the YAML file to write.
        """
        with open(file_name, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(self.quiz.to_dict(), yaml_file, default_flow_style=False, allow_unicode=True)

    def write_json_file(self, file_name: str):
        """
        Write the Quiz object to a JSON file with the specified file name.

        :param file_name: The name of the JSON file to write.
        """
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.quiz.to_dict(), json_file, ensure_ascii=False, indent=4)
