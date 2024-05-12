#!/usr/bin/env python3

import argparse
import signal
import os

from types import FrameType
from sys import version_info


REQUIRED_INTERPRETER_VERSION = 3


def _handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def _get_interpreter_version():
    major, _, _, _, _ = version_info
    return major


def _normalize(string: str) -> str:
    return string.strip().lower()


def _is_empty(file: str) -> bool:
    return os.stat(file).st_size == 0


def _get_leaks(file: str) -> list:
    leaks = []

    with open(args.leak_file, 'r') as f:
        for line in f.readlines():
            normalized_line = _normalize(line)

            if args.csv_separator:
                normalized_line = normalized_line.split(args.csv_separator)[0]

            leaks.append(normalized_line)

    return leaks


def _get_mails(file: str) -> list:
    mails = []

    with open(args.mails_file, 'r') as f:
        for line in f.readlines():
            normalized_line = _normalize(line)
            mails.append(normalized_line)

    return mails


def _get_matches(mails: list, leaks: list) -> list:
    matches = []

    for mail in mails:
        if mail in leaks:
            matches.append(mail)

    return matches


def _print_matches(matches: list) -> None:
    print('wordlist_compare.py')

    if matches:
        print('Matches:')

        for match_ in matches:
            print(f"- {match_}")

    else:
        print('No matches found')


def _write_output_file(ouput_file: str, matches: list) -> None:
    with open(ouput_file, 'w') as f:
        f.write('\n'.join(matches))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)

    if _get_interpreter_version() == REQUIRED_INTERPRETER_VERSION:
        parser = argparse.ArgumentParser(prog='wordlist_compare.py', description='Checks if mails are in a leak file.')
        parser.add_argument('-l', '--leak', help='leak file', dest='leak_file', required=True)
        parser.add_argument('-m', '--mails', help='mails file', dest='mails_file', required=True)
        parser.add_argument('-s', '--separator', help='csv separator used in the leak file', dest='csv_separator', required=False)
        parser.add_argument('-o', '--output', help='emails found in the leak file', dest='output_file', required=False)
        args = parser.parse_args()

        try:
            leak_file_is_empty = _is_empty(args.leak_file)
            mails_file_is_empty = _is_empty(args.mails_file)

            if not leak_file_is_empty and not mails_file_is_empty:
                leaks = _get_leaks(args.leak_file)
                mails = _get_mails(args.mails_file)
                matches = _get_matches(mails, leaks)

                _print_matches(matches)

                if matches and args.output_file:
                    _write_output_file(args.output_file, matches)
            else:
                if leak_file_is_empty:
                    print(f"{args.leak_file} is empty")

                if mails_file_is_empty:
                    print(f"{args.mails_file} is empty")
        except Exception as e:
            print(e)
    else:
        print(f"Requires python{REQUIRED_INTERPRETER_VERSION}")
        exit(0)
