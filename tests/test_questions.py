from utils.questions import MatchingQuestion, MultipleChoiceQuestion, MultipleAnswersQuestion, \
    MultipleShortAnswerQuestion


def test_multiple_short_answer_question():
    q = MultipleShortAnswerQuestion("What is the capital of France?", ["Paris", "paris"])
    assert q.question == "What is the capital of France?"
    assert q.answers == ["Paris", "paris"]
    assert repr(q) == "\nQuestion = What is the capital of France?\nAnswers =\n['Paris', 'paris']\n"


def test_multiple_answers_question():
    q = MultipleAnswersQuestion("Which of the following are vegetables?", ["carrot", "broccoli", "tomato"],
                                ["carrot", "banana", "broccoli", "tomato"])
    assert q.question == "Which of the following are vegetables?"
    assert q.answers == ["carrot", "broccoli", "tomato"]
    assert q.choices == ["carrot", "banana", "broccoli", "tomato"]
    assert repr(
        q) == "\nQuestion = Which of the following are vegetables?\nAnswers =\n['carrot', 'broccoli', 'tomato']\nChoices =\n['carrot', 'banana', 'broccoli', 'tomato']\n"


def test_multiple_choice_question():
    q = MultipleChoiceQuestion("What is the capital of France?", "Paris", ["Berlin", "Rome", "Paris", "Madrid"])
    assert q.question == "What is the capital of France?"
    assert q.answer == "Paris"
    assert q.choices == ["Berlin", "Rome", "Paris", "Madrid"]
    assert repr(
        q) == "\nQuestion = What is the capital of France?\nAnswer = Paris\nChoices = ['Berlin', 'Rome', 'Paris', 'Madrid']\n"


def test_matching_question():
    q = MatchingQuestion("Match the countries with their capitals.",
                         {"France": "Paris", "Spain": "Madrid", "Germany": "Berlin"}, ["Paris", "Madrid", "Berlin"],
                         ["France", "Spain", "Germany"])
    assert q.question == "Match the countries with their capitals."
    assert q.answers == {"France": "Paris", "Spain": "Madrid", "Germany": "Berlin"}
    assert q.answer_bank == ["Paris", "Madrid", "Berlin"]
    assert q.word_bank == ["France", "Spain", "Germany"]
    assert repr(
        q) == "\nQuestion = Match the countries with their capitals.\nAnswers = {'France': 'Paris', 'Spain': 'Madrid', 'Germany': 'Berlin'}\nAnswer bank = ['Paris', 'Madrid', 'Berlin']\nWord bank = ['France', 'Spain', 'Germany']\n"
