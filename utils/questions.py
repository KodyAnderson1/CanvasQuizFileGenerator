from typing import Dict, List


class Question:
    """
    A parent class representing all questions.

    :param question: The text of the question
    """

    def __init__(self, question: str = ""):
        self.question = question
        self.correct_answer: List[str] | str = ""


class MultipleShortAnswerQuestion(Question):
    """
    A class representing a multiple short answer question.

    :param question: The text of the question
    :param answers: A list of correct answers to the question
    """

    def __init__(self, question: str = "", answers: List[str] = None):
        super().__init__(question)
        self.answers: List[str] = answers

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswers =\n{self.answers}\n"


class MultipleAnswersQuestion(Question):
    """
    A class representing a multiple-answers question.

    :param question: The text of the question
    :param answers: A list of correct answers to the question
    :param choices: A list of choices for the question
    """

    def __init__(self, question: str = "", answers: List[str] = None, choices: List[str] = None):
        super().__init__(question)
        self.answers: List[str] = answers
        self.choices: List[str] = choices

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswers =\n{self.answers}\nChoices =\n{self.choices}\n"


class MultipleChoiceQuestion(Question):
    """
     A class representing a multiple-choice question.

     :param question: The text of the question
     :param answer: The correct answer to the question
     :param choices: A list of choices for the question
     """

    def __init__(self, question: str = "", answer: str = "", choices: List[str] = None):
        super().__init__(question)
        self.answer = answer
        self.choices = choices if choices else []

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswer = {self.answer}\nChoices = {self.choices}\n"


class MatchingQuestion(Question):
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
            answers: Dict[str, str] = None,
            answer_bank: List[str] = None,
            word_bank: List[str] = None,
    ):
        super().__init__(question)
        self.answers = answers
        self.answer_bank = answer_bank
        self.word_bank = word_bank

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswers = {self.answers}" \
               f"\nAnswer bank = {self.answer_bank}\nWord bank = {self.word_bank}\n"
