import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

import yaml

from utils.questions import MatchingQuestion, MultipleShortAnswerQuestion, MultipleChoiceQuestion, \
    MultipleAnswersQuestion, ShortAnswerQuestion
from utils.quiz import Quiz
from utils.utils import insert_newlines

# Constants
HEADINGS = {
    "initial": ("=" * 42) + "\n" + (" " * 13) + "QUIZ INFORMATION\n" + ("=" * 42) + "\n",
    "multiple_choice": ("=" * 42) + "\n" + (" " * 9) + "MULTIPLE CHOICE QUESTIONS\n" + ("=" * 42) + "\n\n",
    "multiple_answers": ("=" * 42) + "\n" + (" " * 9) + "MULTIPLE ANSWER QUESTIONS\n" + ("=" * 42) + "\n\n",
    "matching": ("=" * 42) + "\n" + (" " * 14) + "MATCHING QUESTIONS\n" + ("=" * 42) + "\n\n",
    "multiple_short_answers": ("=" * 42) + "\n" + (" " * 6) + "MULTIPLE SHORT ANSWER QUESTIONS\n" + ("=" * 42) + "\n\n",
    "short_answer": ("=" * 42) + "\n" + (" " * 13) + "SHORT ANSWER QUESTIONS\n" + ("=" * 42) + "\n\n",
}
BETA_MESSAGE = " **This section is still being tested. Please report any bugs.**"
BETA_CLASSES = [MultipleShortAnswerQuestion]
DASHES_WITH_NEWLINES = f"\n{'-' * 32}\n\n"
NEWLINE = "\n"
QUESTION_FORMAT_TUPLE = (MultipleShortAnswerQuestion, MultipleAnswersQuestion, ShortAnswerQuestion)
QUIZLET_TERM_DEFINITION_DELIMITER = "\\btd"
QUIZLET_CARDS_DELIMITER = "\\bc"


def format_choices(choices_list):
    return "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(choices_list)])


class QuizFileWriter(ABC):
    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    @abstractmethod
    def write(self, file_path: Path) -> None:
        pass


class TextQuizFileWriter(QuizFileWriter):
    def write(self, file_path: Path) -> None:

        with open(file_path, 'w', encoding='utf-8') as text_file:
            quiz = self.quiz
            mcq, mq = quiz.multiple_choice_questions, quiz.matching_questions
            maq, msaq = quiz.multiple_answer_questions, quiz.multiple_short_answer_questions
            saq = quiz.short_answer_questions
            sections = [
                (len(mcq), HEADINGS["multiple_choice"], "multiple choice questions", mcq),
                (len(mq), HEADINGS["matching"], "matching questions", mq),
                (len(maq), HEADINGS["multiple_answers"], "multiple answers questions", maq),
                (len(msaq), HEADINGS["multiple_short_answers"], "multiple short answer questions", msaq),
                (len(saq), HEADINGS["short_answer"], "short answer questions", saq)
            ]

            text_file.write(HEADINGS["initial"])
            text_file.write(f"Title: {quiz.title}\n\nNumber of questions: {quiz.number_of_questions}\n")

            for count, heading, heading_text, questions in sections:
                if count > 0:
                    text_file.write(self.write_question_summary(questions, heading_text))

            for count, heading, heading_text, questions in sections:
                if count > 0:
                    text_file.write(heading)
                    for q in questions:
                        question = q.question
                        choices = format_choices(q.choices) if hasattr(q, 'choices') else ""

                        if isinstance(q, MatchingQuestion):
                            answer_bank = format_choices(q.answer_bank)
                            word_bank = format_choices(q.word_bank)
                            choices = f"Answer Bank:\n{answer_bank}\n\nWord Bank:\n{word_bank}"

                        if isinstance(q, QUESTION_FORMAT_TUPLE):
                            question = insert_newlines(q.question)

                        answer = self.format_answers(q)
                        text_file.writelines([f"{question}\n{choices}\n\n{answer}{DASHES_WITH_NEWLINES}"])

    def format_answers(self, q):
        if hasattr(q, 'answers') and q.answers or hasattr(q, 'answer') and q.answer:
            if isinstance(q, MatchingQuestion):
                return f"Answer(s):\n{f'{NEWLINE}'.join([f'{key} : {value}' for key, value in q.answers.items()])}"
            elif isinstance(q, MultipleShortAnswerQuestion):
                return f"Answer(s): {f', '.join(q.answers)}"
            elif isinstance(q, MultipleChoiceQuestion):
                return f"Answer: {q.answer}"
            elif isinstance(q, MultipleAnswersQuestion):
                return f"Answer(s):\n{f'{NEWLINE}'.join(q.answers)}"
            elif isinstance(q, ShortAnswerQuestion):
                return f"Answer(s): {q.answer}"
        return ""

    @staticmethod
    def write_question_summary(questions: list, heading_text: str) -> str:
        beta_message = (
            f"{BETA_MESSAGE}"
            if any(isinstance(q, cls) for q in questions for cls in BETA_CLASSES)
            else ""
        )
        return f"Number of {heading_text}: {len(questions)}{beta_message}\n"


class MarkdownQuizFileWriter(QuizFileWriter):
    def write(self, file_path: Path) -> None:

        dashes = f"\n\n{'-' * 3}\n\n"

        with open(file_path, 'w', encoding='utf-8') as text_file:
            quiz = self.quiz
            mcq, mq = quiz.multiple_choice_questions, quiz.matching_questions
            maq, msaq = quiz.multiple_answer_questions, quiz.multiple_short_answer_questions
            saq = quiz.short_answer_questions
            sections = [
                (len(mcq), "Multiple Choice Questions", mcq),
                (len(mq), "Matching Questions", mq),
                (len(maq), "Multiple Answer Questions", maq),
                (len(msaq), "Multiple Short Answer Questions", msaq),
                (len(saq), "Short Answer Questions", saq)
            ]

            text_file.write(f"# {quiz.title}\n\n- Number of questions: {quiz.number_of_questions}\n")

            for count, heading, questions in sections:
                if count > 0:
                    text_file.write(self.write_markdown_summary(questions, heading, count))

            text_file.write(f"\n{dashes}\n")

            for count, heading, questions in sections:
                if count > 0:
                    text_file.write(f"## {heading}\n")
                    for q in questions:
                        question = f"#### {q.question}"
                        choices = format_choices(q.choices) if hasattr(q, 'choices') else ""

                        if isinstance(q, MatchingQuestion):
                            answer_bank = format_choices(q.answer_bank)
                            word_bank = format_choices(q.word_bank)
                            choices = f"#### Answer Bank:\n{answer_bank}\n\n#### Word Bank:\n{word_bank}"
                        elif isinstance(q, QUESTION_FORMAT_TUPLE):
                            question = insert_newlines(q.question)

                        answer = self.format_answers(q)
                        text_file.writelines([f"{question}\n{choices}\n\n{answer}{dashes}"])

    @staticmethod
    def format_answers(q):
        if hasattr(q, 'answers') and q.answers or hasattr(q, 'answer') and q.answer:
            if isinstance(q, MatchingQuestion):
                return f"#### _Answer(s):_{NEWLINE}{''.join([f' {NEWLINE}- {key} : {value}' for key, value in q.answers.items()])}"
            elif isinstance(q, MultipleShortAnswerQuestion):
                return f"#### _Answer(s):_ {f', '.join(q.answers)}"
            elif isinstance(q, MultipleChoiceQuestion):
                return f"#### _Answer(s):_ {q.answer}"
            elif isinstance(q, MultipleAnswersQuestion):
                return f'#### _Answer(s):_{f"".join([f"{NEWLINE}- {choice}" for choice in q.answers])}'
            elif isinstance(q, ShortAnswerQuestion):
                return f"#### _Answer(s):_ {q.answer}"
            return ""

    @staticmethod
    def write_markdown_summary(questions: list, heading: str, count: int) -> str:
        beta_message = (
            f"{BETA_MESSAGE}"
            if any(isinstance(q, cls) for q in questions for cls in BETA_CLASSES)
            else ""
        )
        return f"- Number of [{heading}](#{heading.lower().replace(' ', '-')}): {count}{beta_message}\n"


class QuizletQuizFileWriter(QuizFileWriter):
    def write(self, file_path: Path) -> None:
        """
        Write the Quiz object to a text file with the specified file name and a format for easy quizlet import

        :param file_path: The name of the text file to write.
        """

        with open(file_path, 'w', encoding='utf-8') as text_file:
            quiz = self.quiz
            mcq, mq = quiz.multiple_choice_questions, quiz.matching_questions
            maq, msaq = quiz.multiple_answer_questions, quiz.multiple_short_answer_questions
            saq = quiz.short_answer_questions
            sections = [
                (len(mcq), HEADINGS["multiple_choice"], "multiple choice questions", mcq),
                (len(mq), HEADINGS["matching"], "matching questions", mq),
                (len(maq), HEADINGS["multiple_answers"], "multiple answers questions", maq),
                (len(msaq), HEADINGS["multiple_short_answers"], "multiple short answer questions", msaq),
                (len(saq), HEADINGS["short_answer"], "short answer questions", saq)
            ]

            for count, heading, heading_text, questions in sections:
                if count > 0:
                    for q in questions:
                        question = q.question
                        choices = format_choices(q.choices) if hasattr(q, 'choices') else ""

                        if isinstance(q, MatchingQuestion):
                            choices = self.format_matching(q)
                            text_file.writelines([f"{choices}"])
                        if isinstance(q, MultipleChoiceQuestion):
                            answer = self.format_answers(q)
                            text_file.writelines([f"{question}\n\n{choices}{answer}{QUIZLET_CARDS_DELIMITER}\n"])
                        elif isinstance(q, QUESTION_FORMAT_TUPLE):
                            question = insert_newlines(q.question)
                            answer = self.format_answers(q)
                            text_file.writelines([f"{question}\n\n{choices}{answer}{QUIZLET_CARDS_DELIMITER}\n"])
                        else:
                            logging.warning(f"Question type {type(q)} not supported for Quizlet import")

    @staticmethod
    def format_matching(q: MatchingQuestion):
        return "\n".join([f"{q.question}\n\n{k}\n\n{format_choices(q.answer_bank)}"
                          f"{QUIZLET_TERM_DEFINITION_DELIMITER}{v}{QUIZLET_CARDS_DELIMITER}"
                          for k, v in q.answers.items()])

    @staticmethod
    def format_answers(q):

        if hasattr(q, 'answers') and q.answers or hasattr(q, 'answer') and q.answer:
            if isinstance(q, MatchingQuestion):
                return f"{QUIZLET_TERM_DEFINITION_DELIMITER}{f'{NEWLINE}'.join([f'{key} : {value}' for key, value in q.answers.items()])}"
            elif isinstance(q, MultipleShortAnswerQuestion):
                return f"{QUIZLET_TERM_DEFINITION_DELIMITER}{f', '.join(q.answers)}"
            elif isinstance(q, MultipleChoiceQuestion):
                return f"{QUIZLET_TERM_DEFINITION_DELIMITER}{q.answer}"
            elif isinstance(q, MultipleAnswersQuestion):
                return f"{QUIZLET_TERM_DEFINITION_DELIMITER}{f'{NEWLINE}'.join(q.answers)}"
            elif isinstance(q, ShortAnswerQuestion):
                return f"{QUIZLET_TERM_DEFINITION_DELIMITER}{q.answer}"
        return ""


class YAMLQuizFileWriter(QuizFileWriter):
    def write(self, file_path: Path) -> None:
        with open(file_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(self.quiz.to_dict(), yaml_file, default_flow_style=False, allow_unicode=True)


class JSONQuizFileWriter(QuizFileWriter):
    def write(self, file_path: Path) -> None:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.quiz.to_dict(), json_file, ensure_ascii=False, indent=4)
        pass


class QuizWriter:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def write(self, file_types: Union[List[str], str], output_file: Path) -> None:
        if isinstance(file_types, str):
            file_types = [file_types]

        file_writers = {
            "txt": TextQuizFileWriter,
            "json": JSONQuizFileWriter,
            "yaml": YAMLQuizFileWriter,
            "md": MarkdownQuizFileWriter,
            "qz.txt": QuizletQuizFileWriter
        }

        for file_type in file_types:
            writer_class = file_writers.get(file_type)
            if writer_class:
                output_file_with_ext = output_file.with_suffix(f".{file_type}")
                writer = writer_class(self.quiz)
                writer.write(output_file_with_ext)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
