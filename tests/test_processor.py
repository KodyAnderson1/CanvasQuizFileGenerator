from bs4 import BeautifulSoup

from utils.processor import ProcessQuestions, get_question_text
from utils.quiz import MultipleChoiceQuestion


def test_process_multiple_choice():
    html = """
        <div class="multiple_choice_question">
            <textarea name="question_text">What is the capital of France?</textarea>
            <div class="correct_answer">
                <div class="answer_text">Paris</div>
            </div>
            <div class="answer">
                <div class="answer_text">New York</div>
            </div>
            <div class="answer">
                <div class="answer_text">London</div>
            </div>
            <div class="answer">
                <div class="answer_text">Paris</div>
            </div>
            <div class="answer">
                <div class="answer_text">Madrid</div>
            </div>
        </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    questions = ProcessQuestions(soup).process_multiple_choice()
    assert len(questions) == 1
    question = questions[0]
    assert isinstance(question, MultipleChoiceQuestion)
    assert question.question == 'What is the capital of France?'
    assert question.answer == 'Paris'
    assert question.choices == ['New York', 'London', 'Paris', 'Madrid']


def test_get_question_text():
    html = '<div><textarea name="question_text">This is a test question</textarea></div>'
    soup = BeautifulSoup(html, 'html.parser')
    actual_output = get_question_text(soup)
    expected_output = "This is a test question"
    assert actual_output == expected_output, f"Unexpected output: '{actual_output}'"


def test_get_mc_correct_answer():
    html = '<div><div class="correct_answer"><div class="answer_text">Answer 1</div></div></div>'
    soup = BeautifulSoup(html, 'html.parser')
    actual_output = ProcessQuestions.get_mc_correct_answer(soup)
    expected_output = "Answer 1"
    assert actual_output == expected_output, f"Unexpected output: '{actual_output}'"
