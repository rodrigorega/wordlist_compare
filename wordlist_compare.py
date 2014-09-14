#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

wordlist_compare.py

See README file to get info about this script.

Script Website: https://github.com/rodrigorega/wordlist_compare
Author: Rodrigo Rega <contacto@rodrigorega.es>
License: CC-BY-SA 3.0 license (http://creativecommons.org/licenses/by/3.0/

'''

# ##################### CONFIGURATION START ###################################

# CSV with leaked data. File in format: my@email[leak_file_split]password
leak_file = 'Gmail.txt'

# CSV separator used in leak_file
leak_file_split = ':'

# File with your emails (one per line)
contacts_file = 'my_emails_list.txt'

# File were matched emails in "leak_file" and "contacts_file" "will be saved
match_file = 'my_leaked_emails.txt'

# In normal mode, a 150MB file is using +300MB of RAM, if you are out of RAM,
# use big_file_mode. big_file_mode is slower
big_file_mode = False

# Case sensitive is a little faster
case_sensitive = True

# ##################### CONFIGURATION END #####################################

import time

contacts_file_len = sum(1 for line in open(contacts_file))


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


if __name__ == "__main__":
    '''
    Main

    Return: None
    '''
    process_timer = _print_job_start()
    if big_file_mode:
        search_leak_file_big_file()
    else:
        search_leak_file()
    _print_job_end(process_timer)
