#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""

wordlist_compare.py

Usage:
  wordlist_compare.py -l LEAK_LIST -m MY_LIST [-o OUTPUT_LIST]
                    [-s CSV_SEPARATOR]
  wordlist_compare.py --help

Options:
  -l LEAK_LIST, --leaklist=LEAK_LIST  CSV with leaked data. This file must be
                                      in format: my@email:password

  -m MY_LIST, --mylist=MY_LIST        File with your emails (one per line)

  -o OUTPUT_LIST, --output=OUTPUT_LIST  File were matched emails in LEAK_LIST
                                        and MY_EMAIL_LIST will be saved
                                        [default: my_leaked_emails.txt]
  -s CSV_SEPARATOR, --separator=CSV_SEPARATOR CSV separator used in LEAK_LIST
                                        [default: :]

  -h, --help           Show this help screen.

Script Website: https://github.com/rodrigorega/wordlist_compare
Author: Rodrigo Rega <contacto@rodrigorega.es>
License: CC-BY-SA 3.0 license (http://creativecommons.org/licenses/by/3.0/

"""

import mmap
import os
import sys  # needed for get python version and argv
import time

from docopt import docopt

leaks_file = ''  # Leaked list. Format: my@email[csv_separator]password
accounts_file = ''  # Your email list (one per line)
output_file = ''  # Output file with matched list
separator = ':'  # CSV separator used in leak_file


# noinspection PyShadowingNames
def __search_leaks():
    """
    Compares lines between two files.

    Return: None
    """
    matches = []

    # Check if files are empty
    accounts_file_empty = os.stat(accounts_file).st_size == 0
    leaks_file_empty = os.stat(leaks_file).st_size == 0
    num_accounts = 0

    if not accounts_file_empty and not leaks_file_empty:
        try:
            with open(leaks_file, 'rU') as leak_f:
                mapped_leak_f = mmap.mmap(
                    leak_f.fileno(), 0, mmap.PROT_READ)

                with open(accounts_file, 'rU') as account_f:
                    # TODO: Windowing for files >4gb in python 32b?
                    mapped_account_f = mmap.mmap(account_f.fileno(), 0,
                                                 access=mmap.ACCESS_READ)
                    for account in iter(mapped_account_f.readline, ''):
                        num_accounts = num_accounts + 1
                        __print_job_status(num_accounts,
                                           account.strip())
                        account_formatted = account.strip().lower()

                        mapped_leak_f.seek(0)

                        for leaked_account in iter(mapped_leak_f.readline, ''):
                            current_leaked_account_formatted = leaked_account.split(separator)[0].strip().lower()
                            if account_formatted == current_leaked_account_formatted:
                                matches.append(account.strip())
                                break

            if matches:
                print '\n[!] Matches:'
                __print_list(matches)
                if output_file:
                    __write_to_output_file(matches)
            else:
                print '[*] No matches found.'

        except Exception as ex:
            __handle_exception(ex)
    else:
        if accounts_file_empty:
            print '[!] {0} is empty'.format(accounts_file)
        if leaks_file_empty:
            print '[!] {0} is empty'.format(leaks_file)


def __print_list(l):
    """
    Prints a list in a nice format.

    Return: None
    """
    for item in l:
        print '- {0}'.format(item)
    print


def __handle_exception(ex):
    """
    Handles an exception

    Return: None
    """
    print '[!] {0}'.format(ex)
    __exit_program()


def __write_to_output_file(matches_list):
    """
    Appends a list to output file.

    Return: None
    """
    try:
        with open(output_file, 'w') as f:
            for match in matches_list:
                f.write('{0}\n'.format(match))

    except Exception as ex:
        __handle_exception(ex)


def __print_file_open_error(filename):
    """
    Displays "unable to open file" error.

    Return: filename
    """
    print '[!] Unable to open {0}'.format(filename)


def __exit_program():
    """
    Displays "exiting" message.

    Return: filename
    """
    print '[*] Exiting'
    exit(1)


def __print_job_start():
    """
    Displays a start message.

    Return: start time timer
    """
    job_timer = time.clock()
    print '[*] Starting...'
    return job_timer


def __print_job_end(process_duration):
    """
    Displays a end message.

    Return: None
    """
    print '[*] Finish. Duration: {:0.2f} seconds'.format(time.clock() - process_duration)


def __print_job_status(current_account_number, account):
    """
    Displays a status job info message.

    Return: None
    """
    print '[*] Processing {0}/{1}: {2}'.format(current_account_number, num_accounts, account)


def __print_match_found(matched):
    """
    Displays a  "matched job" message.

    Return: None
    """
    print '[!] Email match in leaked file: {0}'.format(matched)


def __print_job_time(job_timer):
    """
    DIsplays job duration timer.

    Return: None
    """
    print '[-] Search duration: {0.2f} seconds'.format(time.clock() - job_timer)


def __print_python_version_error():
    """
    Displays a python version error.

    Return: None
    """
    print '[!] You must use Python 2,7 or higher'


def __validate_python_version():
    """
    Checks Python version

    Return: True if running version is valid
    """
    major, minor, micro, releaselevel, serial = sys.version_info
    if (major, minor) < (2, 7):
        return False
    else:
        return True


def __get_file_len(f):
    """
    Gets the number of non blank lines of a file.

    Return: number of non blank num_lines in a file.
    """
    num_lines = 0

    with open(f) as inf:
        for line in inf:
            if line.strip():
                num_lines = num_lines + 1

    return num_lines


if __name__ == "__main__":
    '''
    Main

    Return: None
    '''
    if __validate_python_version():
        arguments = docopt(__doc__, version='1.0.0rc2')
        leaks_file = arguments['--leaklist']
        accounts_file = arguments['--mylist']
        output_file = arguments['--output']
        separator = arguments['--separator']
        num_accounts = __get_file_len(accounts_file)

        process_timer = __print_job_start()
        __search_leaks()
        __print_job_end(process_timer)

    else:
        __print_python_version_error()
        __exit_program()
