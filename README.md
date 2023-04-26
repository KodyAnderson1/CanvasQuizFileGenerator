# Quiz File Generation

## NOW WITH...

### Quizlet Support!

- The default format this project saves now is `qz.txt` which is a format intended to copy and paste directly into the
  import feature on a quizlet study set.
- On the Quizlet import screen...
    - For `Between term and definition` click custom and enter `\btd`
    - For `Between cards` click custom and enter `\bc`
- Verify in the preview that everything is being imported correctly.

### Short Answer Support! (Kinda)

- Currently only supports answers that are you answered correctly. Support for incorrect answers will be added in the
  future. Though, will only populate with the correct answers if they are displayed in the HTML file.

### Combined Quizzes!

- The `-cb` flag will combine all `.html` files found in the `raw_html` directory into one quiz item.
- The quiz item will be saved as `combined_quiz.[ext]` in the `output` directory.
- This feature is still in beta, so please report any issues you find, and check the issues tab or known bugs.

---

This project helps parse and save quizzes in various formats, such as text, markdown, JSON, YAML, and a Quizlet import
friendly textfile. Generated from Canvas `.html` files. The `.html` file **must be the quiz itself**, not a submission page
or any other page that loads the quiz as a secondary item.

**Currently supports multiple choice, matching, multiple answer (selection box), short answer, and multiple short answer
questions.**

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
- PyYAML

## Usage

### Installing dependencies

Before dependencies are installed, it is recommended to set up a virtual environment. Instructions for setting up a
virtual environment can be found [below](#setting-up-a-virtual-environment).

A `requirements.txt` file is provided with all the necessary dependencies. To install them, run:

```bash
pip install -r requirements.txt
```

### Running the script

The script processes all `.html` files found in the `raw_html` directory (default path
is `./html/raw_html`) and generate output files based on the specified file type(s).

**Note:** If no file type is specified, the script will default to `qz.txt`.

To use this script, run the following command:

```bash
python main.py [-h] [-rm | -dm] [-f {txt,md,json,yaml, qz.txt} [{txt,md,json,yaml,qz.txt} ...]] [-c CORES] [-cb]
```

Here are the available flags:

- `-h`, `--help`: Show the help message and exit.
- `-f`, `--file_type`: File type(s) to save the quiz as. Options: `txt`, `md`, `json`, `yaml`, `qz.txt`.
  Default: `qz.txt`.
    - Example: `-f json`.
- `-rm`, `--remove_html`: Remove HTML files instead of renaming and moving them. Default: False. Cannot
  use with `-dm`.
- `-dm`, `--dont_move`: Keep HTML files in `raw_html` folder without renaming or moving. Default: False. Cannot use
  with `-rm`.
- `-c`, `--cores`: The number of cores to use for processing the HTML files. Default is half the available cores.
- `-cb`, `--combine`: Combine all quizzes found into one quiz item. Default: False.

Examples:

Create specified file(s) with quiz data, delete .html files, and use 4 cores for processing:

```bash
python main.py -rm -f json yaml txt qz.txt -c 4
```

Create `qz.txt` file(s) with quiz data, rename and move html files to `parsed_html` directory, and use half your
available
cores for processing:

```bash
python main.py
```

Create `qz.txt` file(s) with quiz data, rename and move .html files to `parsed_html` directory, and use 1 core for
processing:

```bash
python main.py -c 1
```

### Changing File Paths

This program uses a `configurations.yaml` file to control the file paths. The paths can be changed to suit your needs.
**DO NOT** change the key names in the file. The `configurations.yaml` file comes preconfigured to work within the
script's directory.

```yaml
directory_paths:
  parsed_html: "can/change/these/paths/html/parsed_html"
  raw_html: "can/change/these/paths/html/raw_html"
  output: "can/change/these/paths/output"
  logs: "./logs"
```

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
