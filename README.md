# Quiz File Generation

### DO NOT TRUST ANSWERS WITH POSITIONAL INDEXING FOR ANY FILE TYPE. ANSWERS CHANGE POSITION WHEN THE QUIZ FILES ARE GENERATED. MANUALLY CHECK AND EDIT THE ANSWERS.

Example:

```txt
What forms the bridge between the software environment and the database environment?
1. Both A and C
2. Second-party interface
3. Third-party Interface
4. Standardized query

Answer: Both A and C
```

Those are the only answers with issues. All others are fine. The name of the generated file is the quiz title for easy
identification.

---

This project was made help to parse, create, and save quizzes in different file formats, such as text, JSON, YAML, and
TOML from a Canvas `.html` file. Currently only works for quizzes with correct answers displayed. The `.html` needs to
be the quiz itself, not a submission page or any other page that "loads" the quiz in as a secondary item.
**Currently, will only output multiple choice, matching and multiple answer (selection box) questions**

## Table of Contents

- [Quiz File Generation](#quiz-file-generation)
    - [Dependencies](#dependencies)
    - [Usage](#usage)
        - [Installing dependencies](#installing-dependencies)
        - [Running the script](#running-the-script)
        - [Changing File Paths](#changing-file-paths)
    - [main.py](#mainpy)
    - [class_structure.py](#class_structurepy)
    - [Setting up a virtual environment](#setting-up-a-virtual-environment)

## Dependencies

- BeautifulSoup
- toml
- PyYAML

## Usage

### Installing dependencies

Before dependencies are installed, it is recommended to set up a virtual environment. Instructions for setting up a
virtual environment can be found [below](#setting-up-a-virtual-environment).

A `requirements.txt` file is provided with all the necessary dependencies. To install them, run the following command:

```bash
pip install -r requirements.txt
```

### Running the script

The script will automatically process all `.html` files found in the `html/raw_html` directory and generate output files
based on the specified file type(s).

**Note:** If no file type is specified, the script will default to saving as a `.txt` file.

To use this script, run the following command:

```bash
python main.py [-h] [-rm | -dm] [-f {txt,json,yaml,toml} [{txt,json,yaml,toml} ...]]
```

Here are the available flags:

- `-h`, `--help`: Show the help message and exit.
- `-f`, `--file_type`: The file type(s) to save the quiz as. Options: `txt`, `json`, `yaml`, `toml`. Default is `txt`.
    - Example: `-f json yaml`.
    - Example: `-f json`.
- `-rm`, `--remove_html`: Flag to remove the HTML files instead of renaming and moving them. Default is False. Cannot
  use with `-dm`.
- `-dm`, `--dont_move`: Flag to keep the HTML files in the `raw_html` folder instead of renaming and moving them.
  Default is
  False. Cannot use with `-rm`.

Examples:

This command will create the specified file(s) with the quiz data and remove/delete the .html files.

```bash
python main.py -rm -f json yaml txt
```

This command will create `.txt` files with the quiz data and rename and move the .html files to
the `parsed_html` directory.

```bash
python main.py
```

---

### Changing File Paths

This program uses a `configurations.yaml` file to control the file paths. The paths can be changed to suit your needs.
**DO NOT** change the key names in the file. The `configurations.yaml` file comes preconfigured to work within the
script's directory.

```yaml
directory_paths:
  windows:
    parsed_html: "can\change\these\paths\html\parsed_html"
    raw_html: "can\change\these\paths\html\raw_html"
    output: "can\change\these\paths\output"
  linux:
    parsed_html: "can/change/these/paths/html/parsed_html"
    raw_html: "can/change/these/paths/html/raw_html"
    output: "can/change/these/paths/output"
```

---

## main.py

This file utilizes the BeautifulSoup library to parse and process a raw HTML file containing quiz data. It then uses the
classes from `quiz.py` to create a `Quiz` object and save it as a file in the specified format. The script
accepts command-line arguments to choose the output file type.

## Utils Directory

### quiz.py

This file contains the following classes:

1. `Quiz`: A class representing a quiz with multiple choice and matching questions.
2. `MultipleChoiceQuestion`: A class representing a multiple-choice question.
3. `MatchingQuestion`: A class representing a matching question.
4. `MultipleAnswerQuestion`: A class representing a multiple answer question.
4. `QuizFileGenerator`: A class for saving quiz objects in different file formats.

### processes.py

This file contains the following classes:

1. `ProcessMultipleAnswers`: A class for processing multiple answer questions.
2. `ProcessMultipleChoice`: A class for processing multiple choice questions.
3. `ProcessMatching`: A class for processing matching questions.

### utils.py

This file contains the following functions:

1. `clean_dict`: Removes all but one whitespace between words, removes newlines, and removes keys with empty values.
2. `clean_list`: Removes all but one whitespace between words, removes newlines from a list, and removes **duplicate**
   items.
3. `clean_string`: Removes all but one whitespace between words and removes newlines from a string.
4. `remove_html_tags`: Removes certain html tags from a string

## Setting up a virtual environment

To set up a virtual environment to run the code, follow these steps:

1. Install `virtualenv` if it's not already installed:

```bash
pip install virtualenv
```

2. Create a virtual environment in the project directory:

```bash
python -m venv venv
```

3. Activate the virtual environment:
    - On Windows:
   ```bash
   venv\Scripts\activate
   ```
    - On macOS and Linux:
   ```bash
   source venv/bin/activate
   ```