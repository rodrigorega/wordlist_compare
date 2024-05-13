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


def _read_file(file: str, csv_separator: str | None) -> list:
    normalized_lines = []

    with open(file, 'r') as f:
        for line in f.readlines():
            normalized_line = _normalize(line)

            if csv_separator:
                normalized_line = normalized_line.split(args.csv_separator)[0]

            normalized_lines.append(normalized_line)

    return normalized_lines


def _get_leaked_mails(mails: list, leaks: list) -> list:
    leaked_mails = []

    for mail in mails:
        if mail in leaks:
            leaked_mails.append(mail)

    return leaked_mails


def _print_leaked_mails(matches: list) -> None:
    print('Matches:')

    for match_ in matches:
        print(f"- {match_}")


def _write_output_file(output_file: str, matches: list) -> None:
    with open(output_file, 'w') as f:
        f.write('\n'.join(matches))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)

    print('wordlist_compare.py')

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
                leaks = _read_file(args.leak_file, args.csv_separator)
                mails = _read_file(args.mails_file, None)
                leaked_mails = _get_leaked_mails(mails, leaks)

                if leaked_mails:
                    _print_leaked_mails(leaked_mails)

                    if args.output_file:
                        _write_output_file(args.output_file, leaked_mails)
                else:
                    print('No matches found')
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
