#!/usr/bin/env python
'''
In 2014-09-10 a file named "google_5000000.7z" was leaked with 5000000 gmail
emails and passwords. I wrote this script to check if my email accounts were
in that leaked file.

No comments in the code by the time, sorry.

Dependencies:
    - leak_file: csv file in format: my@email[leak_file_split]password
    - contacts_file: txt with emails

Usage:
    - Download wordlsit_compare.py
    - Edit configuration options in this script.
    - python compare.py

Output:
    - match_file: csv file with emails matched in "leak_file" and "contacts_file".

Changelog:
    - 2014-09-10: First release.

Author: Rodrigo Rega <contacto@rodrigorega.es>
License: CC-BY-SA 3.0 license (http://creativecommons.org/licenses/by/3.0/    
'''

###################### CONFIGURATION START ###########################

leak_file = 'Gmail.txt'
leak_file_split = ':'
contacts_file = 'my_emails_list.txt'
match_file = 'my_leaked_emails.txt'

# In normal mode, a 150MB file is using +300MB of RAM, if you are out of RAM,
# use big_file_mode. big_file_mode is slower
big_file_mode = False

# Case sensitive is a little faster
case_sensitive = True

###################### CONFIGURATION END #############################

import time

contacts_file_len = sum(1 for line in open(contacts_file))

def search_leak_file():
    '''
    Compare lines in 2 files
    
    Return: None
    '''
    contacts_list = _read_file_to_memory(contacts_file)
    leaks_list  = _read_file_to_memory(leak_file)
    
    for i, contact in enumerate(contacts_list):
        contact = _converte_to_sensitive_if_configured(contact)
        _print_job_status(i,contact)
        t1=time.clock()

        for leak in leaks_list:
            leak = _converte_to_sensitive_if_configured(leak)
            
            #if contact == leak.split(leak_file_split)[0]:
            if leak.startswith(contact):
                _print_match_found(leak)
                _add_to_match_file(leak)
        _print_job_time(t1)

def search_leak_file_big_file():
    '''
    Compare lines in 2 files, version for big files (or for low memory RAM)
    
    Return: None
    '''
    with open(contacts_file, 'rU') as contacts_list:
        for i, contact in enumerate(contacts_list):
            contact = _converte_to_sensitive_if_configured(contact)
            _print_job_status(i,contact)
            t1=time.clock()

            with open(leak_file) as leaks_list:
                for leak in leaks_list:
                    leak = _converte_to_sensitive_if_configured(leak)

                    #if contact == leak.split(leak_file_split)[0]:
                    if leak.startswith(contact):
                        _print_match_found(leak)
                        _add_to_match_file(leak)
            _print_job_time(t1)

def _converte_to_sensitive_if_configured(one_string):
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
    f_content = open(filename, 'rU')
    content_list = f_content.readlines()
    f_content.close()
    return content_list

def _add_to_match_file(data):
    '''
    Append one line to otput file
    
    Return: None
    '''
    f = open(match_file, "a")
    f.write("%s\n" %data)
    f.close()

def _print_job_start():
    '''
    Show start message in console
    
    Return: start time timer
    '''
    t1=time.clock()
    print "[*] Starting...\n"
    return t1

def _print_job_end(t0):
    '''
    Show end message in console
    
    Return: None
    '''
    print("[*] Finish. Duration: %f seconds\n" % (time.clock()-t0))
    
def _print_job_status(contact_number,contact):
    '''
    Show status job info in console
    
    Return: None
    '''
    print "[*] Processing %d of %d: %s" % (contact_number+1, contacts_file_len, contact.split(leak_file_split)[0].lower())
    
def _print_match_found(matched):
    '''
    Show matched job  in console
    
    Return: None
    '''
    print ("[!] Email match in leaked file: %s" % (matched))

def _print_job_time(t1):
    '''
    Show job duration time in console
    
    Return: None
    '''
    print("[-] Search duration: %f seconds\n" % (time.clock()-t1))
        
if __name__ == "__main__":
    '''
    Main
    
    Return: None
    '''
    t0 = _print_job_start()
    if big_file_mode:
        search_leak_file_big_file()
    else:
        search_leak_file()
    _print_job_end(t0)
