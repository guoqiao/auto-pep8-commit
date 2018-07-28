# Auto PEP8 Commit

## What
This repo is a simple Python script, which does:

- Run flake8 on your source code
- Group violations by Error Code
- Sort Error Code by violation count, smaller first
- Loop through each Error Code
- Run `autopep8` for that Error Code
- Fix each violation in place
- Commit each affected file to git

## Why
One day, your team decide to follow PEP8 code style for Python.
You run `flake8`, and discover thousands of errors.
It's not possible to do it manually, in limited time frame.

An example in my project:

    ...
    605   E402 module level import not at top of file
    606   E226 missing whitespace around arithmetic operator
    706   E122 continuation line missing indentation or outdented
    849   E203 whitespace before ':'
    916   F401 'time' imported but unused
    1038  E127 continuation line over-indented for visual indent
    1171  E231 missing whitespace after ','
    1258  E221 multiple spaces before operator
    1564  E251 unexpected spaces around keyword / parameter equals
    1759  E302 expected 2 blank lines, found 1
    2099  F405 'normalise_int32' may be undefined, or defined from star imports: samba.common
    12083 W191 indentation contains tabs
    12448 E501 line too long (92 > 79 characters)
    ...

You decide to automate it with tools like `autopep8`.
To avoid making huge commit, you will format files by each Error Code.
(Each one still need a human double check or adjustment)
And you would like to start from Error Code with smaller violation count.
Thus you don't get stuck in a monster one, and make progress quickly.

At last, if some of the Error Code is too much job to fix, you can choose to
ignore it in your flake8 config.

As you can see, this whole process can be automated with a script.

## How
The script used the `subprocess.run` method, which is introduced in Python 3.5.

Since this script will commit to your git, you'd better create a branch
first for it to work on.

Also, it will respect `.flake8` config file like `flake8` does.

    cd /path/to/code
    /path/to/auto-pep8-commit.py

or:

    /path/to/auto-pep8-commit.py /path/to/code

