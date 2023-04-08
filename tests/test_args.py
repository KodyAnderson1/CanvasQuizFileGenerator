import argparse


def test_file_type_arg():
    parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")
    parser.add_argument(
        "-f", "--file_type", type=str, default="txt", nargs="+",
        choices=["txt", "json", "yaml", "md"],
        help="The file type to save the quiz as. Options: txt, md, json, yaml."
    )

    args = parser.parse_args(["-f", "txt"])
    assert args.file_type == ["txt"]

    args = parser.parse_args(["-f", "md"])
    assert args.file_type == ["md"]

    args = parser.parse_args(["-f", "json", "yaml"])
    assert args.file_type == ["json", "yaml"]


def test_remove_html_arg():
    parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")

    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        "-rm", "--remove_html", action="store_true",
        help="Flag to remove the HTML files instead of renaming and moving them. "
             "Selecting this flag will prevent the use of the -dm flag."
    )

    exclusive_group.add_argument(
        "-dm", "--dont_move", action="store_true",
        help="Flag to keep .html files in the origin directory with their original names. "
             "Selecting this flag will prevent the use of the -rm flag."
    )

    args = parser.parse_args(["-rm"])
    assert args.remove_html == True
    assert args.dont_move == False

    args = parser.parse_args([])
    assert args.remove_html == False
    assert args.dont_move == False


def test_dont_move_arg():
    parser = argparse.ArgumentParser(description="Save a quiz as a specific file type.")

    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        "-rm", "--remove_html", action="store_true",
        help="Flag to remove the HTML files instead of renaming and moving them. "
             "Selecting this flag will prevent the use of the -dm flag."
    )

    exclusive_group.add_argument(
        "-dm", "--dont_move", action="store_true",
        help="Flag to keep .html files in the origin directory with their original names. "
             "Selecting this flag will prevent the use of the -rm flag."
    )

    args = parser.parse_args(["-dm"])
    assert args.remove_html == False
    assert args.dont_move == True

    args = parser.parse_args([])
    assert args.remove_html == False
    assert args.dont_move == False
