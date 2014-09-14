#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

wordlist_compare.py

Usage:
  wordlist_compare.py -l LEAK_LIST -m MY_LIST [-o OUTPUT_LIST]
                      [-s CSV_SEPARATOR] [--lowmemorymode] [--casesensitive]
  wordlist_compare.py --help

Options:
  -l LEAK_LIST, --leaklist=LEAK_LIST  CSV with leaked data. This file must be
                                      in format: my@email:password

  -m MY_LIST, --mylist=MY_LIST        File with your emails (one per line)

  -o OUTPUT_LIST, --output=OUTPUT_LIST  File were matched emails in LEAK_LIST
                                        and MY_EMAIL_LIST will be saved
                                        [default: my_leaked_emails.txt]

  -s CSV_SEPARATOR, --separator=CSV_SEPARATOR  CSV separator used in LEAK_LIST
                                               [default: :]

  -w, --lowmemorymode  Use this if you are comparing big files and your PC is
                       out of RAM. This mode is solwer. [default: False]

  -c, --casesensitive  Enable case sensitive. This is faster. [default: False]

  -h, --help           Show this help screen.

Script Website: https://github.com/rodrigorega/wordlist_compare
Author: Rodrigo Rega <contacto@rodrigorega.es>
License: CC-BY-SA 3.0 license (http://creativecommons.org/licenses/by/3.0/

'''

import time
import sys  # needed for get python version and argv
from docopt import docopt


leak_file = '' # Leaked list. Format: my@email[leak_file_split]password
leak_file_split = '' # CSV separator used in leak_file
contacts_file = ''# Your email list (one per line)
match_file = '' # Output file with matched list
case_sensitive = '' # Case sensitive is a little faster
# In normal mode, a 150MB file is using +300MB of RAM, if you are out of RAM,
# use big_file_mode. big_file_mode is slower
big_file_mode = ''


def search_leak_file():
    '''
    Compare lines in 2 files

    Return: None
    '''
    contacts_list = _read_file_to_memory(contacts_file)
    leaks_list = _read_file_to_memory(leak_file)

    for i, contact in enumerate(contacts_list):
        contact = _check_case_sensitive(contact)
        _print_job_status(i, contact)
        job_timer = time.clock()

        for leak in leaks_list:
            leak = _check_case_sensitive(leak)

            # if contact == leak.split(leak_file_split)[0]:
            if leak.startswith(contact):
                _print_match_found(leak)
                _add_to_match_file(leak)
        _print_job_time(job_timer)


def search_leak_file_big_file():
    '''
    Compare lines in 2 files, version for big files (or for low memory RAM)

    Return: None
    '''
    with open(contacts_file, 'rU') as contacts_list:
        for i, contact in enumerate(contacts_list):
            contact = _check_case_sensitive(contact)
            _print_job_status(i, contact)
            job_timer = time.clock()

            with open(leak_file) as leaks_list:
                for leak in leaks_list:
                    leak = _check_case_sensitive(leak)

                    # if contact == leak.split(leak_file_split)[0]:
                    if leak.startswith(contact):
                        _print_match_found(leak)
                        _add_to_match_file(leak)
            _print_job_time(job_timer)


def _check_case_sensitive(one_string):
    '''
    Convert string to lower if configured

    Return: same string or lowered
    '''
    if case_sensitive:
        return one_string.rstrip()
    else:
        return one_string.lower().rstrip()


def _read_file_to_memory(filename):
    '''
    Get file contents and store it in RAM

    Return: contents of readed file
    '''
    try:
        content_list = open(filename, 'rU').readlines()
        return content_list
    except IOError:
        _print_file_open_error(filename)
        _print_exiting()
        exit(1)


def _add_to_match_file(data):
    '''
    Append one line to otput file

    Return: None
    '''

    try:
        f_matchfile = open(match_file, "a")
    except IOError:
        _print_file_open_error(match_file)
        _print_exiting()
        exit(1)

    try:
        f_matchfile.write("%s\n" % data)
    except IOError:
        _print_file_open_error(match_file)
        _print_exiting()
        exit(1)

    f_matchfile.close()


def _print_file_open_error(filename):
    '''
    Show unable to open in console

    Return: filename
    '''
    print "[!] Unable to open  %s " % filename


def _print_file_write_error(filename):
    '''
    Show write error in console

    Return: filename
    '''
    print "[!] Unable to write to  %s " % filename


def _print_exiting():
    '''
    Show exiting in console

    Return: filename
    '''
    print "[*] Exiting"


def _print_job_start():
    '''
    Show start message in console

    Return: start time timer
    '''
    job_timer = time.clock()
    print "[*] Starting...\n"
    return job_timer


def _print_job_end(process_duration):
    '''
    Show end message in console

    Return: None
    '''
    print "[*] Finish. Duration: %f seconds\n" % (time.clock()
                                                  - process_duration)


def _print_job_status(contact_number, contact):
    '''
    Show status job info in console

    Return: None
    '''
    print "[*] Processing %d of %d: %s" % (contact_number + 1,
                                           contacts_file_len,
                                           contact.split(leak_file_split)
                                           [0].lower())


def _print_match_found(matched):
    '''
    Show matched job  in console

    Return: None
    '''
    print "[!] Email match in leaked file: %s" % (matched)


def _print_job_time(job_timer):
    '''
    Show job duration time in console

    Return: None
    '''
    print "[-] Search duration: %f seconds\n" % (time.clock()-job_timer)


def _print_python_version_error():
    '''
    Show python version error

    Return: None
    '''
    print '[!] You must use Python 2,7 or higher'


def _validate_python_version():
    '''
    Check Python version

    Return: True if running version is valid
    '''
    major, minor, micro, releaselevel, serial = sys.version_info
    if (major, minor) < (2, 7):
        return False
    else:
        return True


def _start_process():
    '''
    Select work mode and start process

    Return: None
    '''
    if big_file_mode:
        search_leak_file_big_file()
    else:
        search_leak_file()


if __name__ == "__main__":
    '''
    Main

    Return: None
    '''
    if _validate_python_version():
        arguments = docopt(__doc__, version='1.0.0rc2')
        big_file_mode = arguments['--lowmemorymode']
        case_sensitive = arguments['--casesensitive']
        leak_file = arguments['--leaklist']
        contacts_file = arguments['--mylist']
        leak_file_split = arguments['--separator']
        match_file = arguments['--output']
        contacts_file_len = sum(1 for line in open(contacts_file))

        _start_process()
        process_timer = _print_job_start()
        _print_job_end(process_timer)

    else:
        _print_python_version_error()
        _print_exiting()
        sys.exit(2)
