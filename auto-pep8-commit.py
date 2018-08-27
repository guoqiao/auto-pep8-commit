#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from os.path import abspath, dirname, join, normpath

ERROR_MARK = 'PEP8'

# default: '%(path)s:%(row)d:%(col)d: %(code)s %(text)s'
# use | to split, avoid space trouble in text
ERROR_FORMAT = ERROR_MARK + "|%(code)s|%(path)s|%(text)s"


def debug(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def main():

    parser = argparse.ArgumentParser(
        description='Fix PEP8 by each Error Code and commit')

    parser.add_argument(
        '-p', '--path', help='path to code')

    args = parser.parse_args()

    if args.path:
        # cd into dir, then flake8 will respect .flake8 there
        os.chdir(args.path)

    cwd = os.getcwd()

    debug('working in {}...'.format(cwd))

    tree = {}

    def run(cmd):
        """Run cmdline and get result"""
        debug('\nsubprocess.run:', cmd)
        return subprocess.run(
            cmd, stdout=subprocess.PIPE, cwd=cwd
        ).stdout.decode('utf-8')

    cmd = [
        "python",
        "-m",
        "pycodestyle",
        "--format={}".format(ERROR_FORMAT),
    ]
    stdout = run(cmd)

    lines = stdout.splitlines()
    for line in lines:
        if line.startswith(ERROR_MARK):
            _, code, path, text = line.split('|')
            code = code.strip()
            path = path.strip()
            text = text.strip()
            if code in tree:
                tree[code]['paths'].add(path)
                tree[code]['count'] = len(tree[code]['paths'])
            else:
                tree[code] = {
                    'code': code,
                    'text': text,
                    'count': 1,
                    'paths': {path},
                }

    items = sorted(tree.values(), key=lambda item: item['code'])

    for item in items:
        debug('\nautopep8: {code} {count}: {text}\n'.format(**item))

        paths = list(item['paths'])

        for path in paths:
            debug(path)

        cmd = [
            "python",
            "-m",
            "autopep8",
            "--aggressive",
            "--aggressive",  # repeat
            "--in-place",
            "--select={}".format(item['code']),
        ]
        run(cmd + paths)

        cmd = [
            "git",
            "add",
            "--update",  # stop git to add new files
        ]
        run(cmd + paths)

        cmd = [
            "git",
            "commit",
            "--no-verify",
            "--signoff",
            "--message",
            "PEP8: fix {}: {}".format(item['code'],
                                      item['text']),
        ]
        run(cmd)


if __name__ == '__main__':
    main()
