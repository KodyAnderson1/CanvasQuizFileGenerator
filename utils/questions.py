from typing import Dict, List


class Question:
    """
    A parent class representing all questions.

    :param question: The text of the question
    """

    def __init__(self, question: str = ""):
        self.question = question

    def __eq__(self, other):
        if not isinstance(other, Question):
            return False
        return self.question == other.question

    def __hash__(self):
        return hash(self.question)


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

    def __eq__(self, other):
        if not isinstance(other, MultipleShortAnswerQuestion):
            return False
        return super().__eq__(other) and self.answers == other.answers

    def __hash__(self):
        return hash((super().__hash__(), tuple(self.answers)))


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

    def __eq__(self, other):
        if not isinstance(other, MultipleAnswersQuestion):
            return False
        return super().__eq__(other) and self.answers == other.answers and self.choices == other.choices

    def __hash__(self):
        return hash((super().__hash__(), tuple(self.answers), tuple(self.choices)))


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

    def __eq__(self, other):
        if not isinstance(other, MultipleChoiceQuestion):
            return False
        # return super().__eq__(other) and self.answer == other.answer and self.choices == other.choices
        return super().__eq__(other) and self.choices == other.choices

    def __hash__(self):
        return hash((super().__hash__(), tuple(self.choices)))


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

    def __eq__(self, other):
        if not isinstance(other, MatchingQuestion):
            return False
        return (
                super().__eq__(other)
                and self.answers == other.answers
                and self.answer_bank == other.answer_bank
                and self.word_bank == other.word_bank
        )

    def __hash__(self):
        return hash((
            super().__hash__(),
            frozenset(self.answers.items()),
            tuple(self.answer_bank),
            tuple(self.word_bank),
        ))


class ShortAnswerQuestion(Question):
    """
    A class representing a short answer question.

    :param question: The text of the question
    :param answer: The correct answer to the question
    """

    def __init__(self, question: str = "", answer: str = ""):
        super().__init__(question)
        self.answer = answer

    def __repr__(self):
        return f"\nQuestion = {self.question}\nAnswer = {self.answer}\n"

    def __eq__(self, other):
        if not isinstance(other, ShortAnswerQuestion):
            return False
        return super().__eq__(other) and self.answer == other.answer

    def __hash__(self):
        return hash((super().__hash__(), self.answer))
