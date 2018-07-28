#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from os.path import abspath, dirname, join, normpath

FLAKE8_MARK = 'FLAKE8'

# default: '%(path)s:%(row)d:%(col)d: %(code)s %(text)s'
# use | to split, avoid space trouble in text
FLAKE8_FORMAT = FLAKE8_MARK + "|%(code)s|%(path)s|%(text)s"


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
        "flake8",
        "--format={}".format(FLAKE8_FORMAT),
    ]
    stdout = run(cmd)

    lines = stdout.splitlines()
    for line in lines:
        if line.startswith(FLAKE8_MARK):
            _, code, path, text = line.split('|')
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

    items = sorted(tree.values(), key=lambda item: item['count'])

    for item in items:
        debug('\nautopep8: {code} {count}: {text}\n'.format(**item))

        paths = list(item['paths'])

        for path in paths:
            debug(path)

        cmd = [
            "python",
            "-m",
            "autopep8",
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
            "--signoff",
            "--message",
            "PEP8: fix {}: {}".format(item['code'],
                                      item['text']),
        ]
        run(cmd)


if __name__ == '__main__':
    main()
