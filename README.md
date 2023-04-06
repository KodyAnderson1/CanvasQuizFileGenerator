# Quiz File Generation

## NOW WITH QUIZLET IMPORT SUPPORT

- The default format this project saves now is `qz.txt` which is a format intended to copy and paste directly into the import feature on a quizlet study set.
- At the moment, the delimiters are hard-coded, but future iterations of the project will probably include a flag to determine them yourself.
- On the import screen...
  - For `Between term and definition` click custom and enter `\btd`
  - For `Between cards` click custom and enter `\bc`
- Verify in the preview that everything is being imported correctly.

---

**BE CAREFUL WITH ANSWERS THAT USE POSITIONAL INDEXING. ANSWERS USED TO CHANGE POSITION WHEN THE QUIZ FILES ARE
GENERATED. MANUALLY CHECK AND EDIT THE ANSWERS.**

This should no longer be an issue, but be aware of the potential for issues.

Example:

```txt
What forms the bridge between the software environment and the database environment?
1. Both A and C
2. Second-party interface
3. Third-party Interface
4. Standardized query

Answer: Both A and C
```

---

This project was made help to parse, create, and save quizzes in different file formats, such as text, markdown, JSON,
YAML, and have quizlet import support from a Canvas `.html` file. The `.html` needs to be the quiz itself, not a submission page or any other
page that "loads" the quiz in as a secondary item.

**Currently, will only output multiple choice, matching, multiple answer (selection box), and multiple short answer questions**

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

A `requirements.txt` file is provided with all the necessary dependencies. To install them, run the following command:

```bash
pip install -r requirements.txt
```

### Running the script

The script will automatically process all `.html` files found in the `raw_html` directory (default path is `./html/raw_html`) and generate output files based on the specified file type(s).

**Note:** If no file type is specified, the script will default to saving as a `qz.txt` file.

To use this script, run the following command:

```bash
python main.py [-h] [-rm | -dm] [-f {txt,md,json,yaml, qz.txt} [{txt,md,json,yaml,qz.txt} ...]]
```

Here are the available flags:

- `-h`, `--help`: Show the help message and exit.
- `-f`, `--file_type`: The file type(s) to save the quiz as. Options: `txt`, `md`, `json`, `yaml`, `qz.txt`. Default is `qz.txt`.
  - Example: `-f json`.
- `-rm`, `--remove_html`: Flag to remove the HTML files instead of renaming and moving them. Default is False. Cannot
  use with `-dm`.
- `-dm`, `--dont_move`: Flag to keep the HTML files in the `raw_html` folder instead of renaming and moving them.
  Default is False. Cannot use with `-rm`.

Examples:

This command will create the specified file(s) with the quiz data and remove/delete the .html files.

```bash
python main.py -rm -f json yaml txt qz.txt
```

This command will create `qz.txt` file(s) with the quiz data. It will also **rename and move** the .html files to the `parsed_html`
directory.

```bash
python main.py
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
