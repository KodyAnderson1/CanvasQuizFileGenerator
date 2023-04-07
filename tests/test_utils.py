from utils.utils import insert_newlines, clean_html, remove_duplicates, clean_input
from bs4 import BeautifulSoup
import pytest


def test_insert_newlines_no_parentheses():
    text = "This is a sentence. This is another sentence. This is a question? This is an exclamation!"
    expected_output = "This is a sentence.\nThis is another sentence.\nThis is a question?\nThis is an exclamation!"
    actual_output = insert_newlines(text)
    assert actual_output.strip() == expected_output.strip(), f"Unexpected output: '{actual_output}'"


def test_insert_newlines_with_parentheses():
    text = "This is a sentence. This is (another sentence). This is a question? This is an exclamation!"
    expected_output = "This is a sentence.\nThis is (another sentence).\nThis is a question?\nThis is an exclamation!"
    actual_output = insert_newlines(text)
    assert actual_output.strip() == expected_output.strip(), f"Unexpected output: '{actual_output}'"


def test_insert_newlines_with_ie_or_eg():
    text = "This is a sentence. This is another sentence. This is a question? This is an exclamation! i.e. This is an example."
    expected_output = "This is a sentence.\nThis is another sentence.\nThis is a question?\nThis is an exclamation! i.e.\nThis is an example."
    actual_output = insert_newlines(text)
    next_token = ' '.join(text.split()[7:9])  # Get the next token after 'i.e.'
    assert actual_output.strip() == expected_output.strip(), f"Unexpected output: '{actual_output}', next token: '{next_token}'"


def test_insert_newlines_no_periods():
    text = "This is a sentence without any periods or questions marks"
    expected_output = "This is a sentence without any periods or questions marks"
    actual_output = insert_newlines(text)
    assert actual_output.strip() == expected_output.strip(), f"Unexpected output: '{actual_output}'"


def test_insert_newlines_empty_string():
    text = ""
    expected_output = ""
    actual_output = insert_newlines(text)
    assert actual_output.strip() == expected_output.strip(), f"Unexpected output: '{actual_output}'"


def test_remove_duplicates_empty():
    input_list = []
    expected_output = []
    assert remove_duplicates(input_list) == expected_output


def test_remove_duplicates_single():
    input_list = [1]
    expected_output = [1]
    assert remove_duplicates(input_list) == expected_output


def test_remove_duplicates_multiple():
    input_list = [1, 2, 3, 2, 4, 3]
    expected_output = [1, 2, 3, 4]
    assert remove_duplicates(input_list) == expected_output


def test_remove_duplicates_strings():
    input_list = ["apple", "banana", "cherry", "banana", "cherry"]
    expected_output = ["apple", "banana", "cherry"]
    assert remove_duplicates(input_list) == expected_output


def test_remove_duplicates_mixed():
    input_list = [1, "apple", 2, "banana", 3, "cherry", 2, "banana", "cherry"]
    expected_output = [1, "apple", 2, "banana", 3, "cherry"]
    assert remove_duplicates(input_list) == expected_output


def test_clean_input_string():
    input_str = "   This   is \n   a \n   test.  "
    expected_output = "This is a test."
    assert clean_input(input_str) == expected_output


def test_clean_input_dict():
    input_dict = {"   key   ": "   value  ", "   key2   ": "   value2   ", "key3": " "}
    expected_output = {"key": "value", "key2": "value2"}
    assert clean_input(input_dict) == expected_output


def test_clean_input_list():
    input_list = ["   item1   ", "  ", "item2   ", "item3\nitem4"]
    expected_output = ["item1", "item2", "item3 item4"]
    assert clean_input(input_list) == expected_output


@pytest.fixture
def sample_html():
    return '''
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Test Page</h1>
            <img src="test.jpg" alt="Test Image">
            <p>This is a paragraph.</p>
            <input type="text" name="username">
            <p>This is another paragraph.&nbsp;This is a third sentence.</p>
        </body>
        </html>
    '''


def test_clean_html_empty_string():
    assert clean_html('') == ''


def test_clean_html_invalid_input():
    assert clean_html(123) == 123
    assert clean_html(None) == None

# def test_clean_html_remove_img(sample_html):
#     expected_output = '<html>\n<head>\n<title>Test Page</title>\n</head>\n<body>\n<h1>Test Page</h1>\n<p>This is a paragraph.</p>\n\n<p>This is another paragraph. This is a third sentence.</p>\n</body>\n</html>'
#     soup = BeautifulSoup(sample_html, 'html.parser')
#     actual_output = str(clean_html(soup))
#     assert actual_output == expected_output


# def test_clean_html_replace_input(sample_html):
#     expected_output = '<html>\n<head>\n<title>Test Page</title>\n</head>\n<body>\n<h1>Test Page</h1>\n<p>This is a paragraph.</p>\n\n<p>This is another paragraph. This is a third sentence.</p>\n</body>\n</html>'
#     soup = BeautifulSoup(sample_html, 'html.parser')
#     actual_output = str(clean_html(soup))
#     assert actual_output == expected_output
#
#
# def test_clean_html_remove_nbsp(sample_html):
#     expected_output = '<html>\n<head>\n<title>Test Page</title>\n</head>\n<body>\n<h1>Test Page</h1>\n<p>This is a paragraph.</p>\n\n<p>This is another paragraph. This is a third sentence.</p>\n</body>\n</html>'
#     soup = BeautifulSoup(sample_html, 'html.parser')
#     actual_output = str(clean_html(soup))
#     assert actual_output.strip() == expected_output.strip()
