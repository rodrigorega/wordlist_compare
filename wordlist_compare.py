#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

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

'''

import time
import sys  # needed for get python version and argv
from docopt import docopt
import mmap
import os


leaks_file = '' # Leaked list. Format: my@email[csv_separator]password
accounts_file = ''# Your email list (one per line)
output_file = '' # Output file with matched list
leak_file_split = ':' # CSV separator used in leak_file


def __search_leak_file(): # TODO: Rename to __search_leaks
    '''
    Compare lines between two files.
    
    Return: None
    '''
    matches = []
    
    #Check if files are empty
    accounts_file_empty = os.stat(accounts_file).st_size == 0
    leaks_file_empty = os.stat(leaks_file).st_size == 0
    
    if (not accounts_file_empty and not leaks_file_empty):
        try:
            with open(leaks_file, 'rU') as lf:
                mlf = mmap.mmap(lf.fileno(), 0, prot=mmap.PROT_READ)

                with open(accounts_file,'rU') as af:
                    # memory-map the file, size 0 means whole size
                    #TODO: Windowing for files >4gb in python 32b?
                    maf = mmap.mmap(af.fileno(), 0, prot=mmap.PROT_READ)
                    for account in iter(maf.readline, ''):
                        current_account_fomatted = account.strip().lower()
                        
                        mlf.seek(0)
                        
                        for leaked_account in iter(mlf.readline, ''):
                            current_leaked_account_formatted = leaked_account.split(leak_file_split)[0].strip().lower()
                            if(current_account_fomatted == current_leaked_account_formatted):
                                matches.append(account.strip())
                                break

            if(matches):
                __print_list(matches)
                if(output_file):
                    __write_to_output_file(matches)
            else:
                print '[*] No matches found.' 
                
        except Exception as ex:
            __handle_Exception(ex)
    else:
        if accounts_file_empty:
            print '[!] {0} is empty'.format(accounts_file)
        if leaks_file_empty:
            print '[!] {0} is empty'.format(leaks_file)

def __print_list(l):
    '''
    Prints a list in a nice format.
    
    Return: None
    '''
    for item in l:
        print '- {0}'.format(item)
        
def __handle_Exception(ex):
    '''
    Handles an exception
    
    Return: None
    '''
    print '[!] {0}'.format(ex)
    __exit_program()
        

def __write_to_output_file(matches_list):
    '''
    Append one line to otput file

    Return: None
    '''
    try:
        with open(output_file, 'w') as of:
            for match in matches_list:
                of.write('{0}\n'.format(match))

    except Exception as ex:
        __handle_Exception(ex)


def __print_file_open_error(filename):
    '''
    Show unable to open in console

    Return: filename
    '''
    print '[!] Unable to open {0}'.format(filename)


def __exit_program():
    '''
    Show exiting in console

    Return: filename
    '''
    print '[*] Exiting'
    exit(1)


def __print_job_start():
    '''
    Show start message in console

    Return: start time timer
    '''
    job_timer = time.clock()
    print '[*] Starting...'
    return job_timer


def __print_job_end(process_duration):
    '''
    Show end message in console

    Return: None
    '''
    print '[*] Finish. Duration: {:0.2f} seconds'.format(time.clock()
                                                        - process_duration)


def __print_job_status(contact_number, contact):
    '''
    Show status job info in console

    Return: None
    '''
    print '[*] Processing {0} of {1}: {2}'.format(contact_number + 1,
                                                  accounts_file_lines,
                                                  contact.split(csv_separator)
                                                  [0].lower())


def __print_match_found(matched):
    '''
    Show matched job  in console

    Return: None
    '''
    print '[!] Email match in leaked file: {0}'.format(matched)


def __print_job_time(job_timer):
    '''
    Show job duration time in console

    Return: None
    '''
    print '[-] Search duration: {0.2f} seconds'.format(time.clock()-job_timer)


def __print_python_version_error():
    '''
    Show python version error

    Return: None
    '''
    print '[!] You must use Python 2,7 or higher'


def __validate_python_version():
    '''
    Check Python version

    Return: True if running version is valid
    '''
    major, minor, micro, releaselevel, serial = sys.version_info
    if (major, minor) < (2, 7):
        return False
    else:
        return True


def __start_process():
    '''
    Select work mode and start process

    Return: None
    '''
    __search_leak_file()
        
        
def __get_file_len(f):
    '''
    __get_file_len
    
    Return: number of non blank num_lines in file.
    '''
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
        leak_file_split = arguments['--separator']
        accounts_file_lines = __get_file_len(accounts_file)

        process_timer = __print_job_start()
        __start_process()
        __print_job_end(process_timer)

    else:
        __print_python_version_error()
        __exit_program()
