#!/usr/bin/env python3

import argparse
import signal
from operator import methodcaller
from sys import version_info
from tqdm import tqdm
from types import FrameType

REQUIRED_INTERPRETER_VERSION = 3


def _handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def _get_interpreter_version():
    major, _, _, _, _ = version_info
    return major


def _read_file(file: str, csv_separator: str | None) -> list:
    with open(file, 'r') as f:
        if csv_separator:
            return [item[0] for item in map(methodcaller("split", csv_separator), f.readlines())]
        else:
            return f.readlines()


def _normalize(string: str) -> str:
    try:
        mail = string.strip().lower()
        user, domain = mail.split('@')
        normalized_user = user.replace('.', '')

        return f"{normalized_user}@{domain}"
    except ValueError:
        print(f"Malformed mail: {string.rstrip()}")


def _get_leaked_mails(mails: list, leaks: list) -> list:
    leaked_mails = []
    normalized_mails = map(_normalize, mails)
    normalized_leaks = map(_normalize, leaks)

    for mail in tqdm(normalized_mails):
        if mail in normalized_leaks and mail not in leaked_mails:
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
    print('* \'foo.bar@mail.com\' will be treated as \'foobar@mail\'.\n')

    if _get_interpreter_version() == REQUIRED_INTERPRETER_VERSION:
        parser = argparse.ArgumentParser(prog='wordlist_compare.py', description='Checks if mails are in a leak file.')
        parser.add_argument('-l', '--leak', help='leak file', dest='leak_file', required=True)
        parser.add_argument('-m', '--mails', help='mails file', dest='mails_file', required=True)
        parser.add_argument('-s', '--separator', help='csv separator used in the leak file', dest='csv_separator', required=False)
        parser.add_argument('-o', '--output', help='emails found in the leak file', dest='output_file', required=False)
        args = parser.parse_args()

        if args.leak_file != args.mails_file:
            try:
                print()

                mails = _read_file(args.mails_file, None)
                leaks = _read_file(args.leak_file, args.csv_separator)
                leaked_mails = _get_leaked_mails(mails, leaks)

                if leaked_mails:
                    _print_leaked_mails(leaked_mails)

                    if args.output_file:
                        _write_output_file(args.output_file, leaked_mails)
                else:
                    print('No matches found')
            except FileNotFoundError as fee:
                print(f"'{fee.filename}' no such file or directory")
            except Exception as e:
                print(e)
        else:
            print(f"Leaks file and mails file are the same: '{args.leak_file}'")
    else:
        print(f"Requires python{REQUIRED_INTERPRETER_VERSION}")
        exit(0)
