# wordlist_compare

## Why?

In 2014-09-10 a file named "google_5000000.7z" was leaked with 5000000 gmail emails and passwords.  
I wrote this script to check if my email accounts were in that leaked file.

## Usage

```
usage: wordlist_compare.py [-h] -l LEAK_FILE -m MAILS_FILE [-s CSV_SEPARATOR] [-o OUTPUT_FILE]

Checks if mails are in a leak file.

options:
  -h, --help            show this help message and exit
  -l LEAK_FILE, --leak LEAK_FILE
                        leak file
  -m MAILS_FILE, --mails MAILS_FILE
                        mails file
  -s CSV_SEPARATOR, --separator CSV_SEPARATOR
                        csv separator used in the leak file
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        emails found in the leak file
```

## Requirements

* tqdm

## About wordlist_compare

Script Website: [https://github.com/rodrigorega/wordlist_compare](https://github.com/rodrigorega/wordlist_compare)  
License: [CC-BY-SA 3.0](http://creativecommons.org/licenses/by/3.0)  

## Author

Author: Rodrigo Rega <contacto@rodrigorega.es>  

## Contributors

* [Rubén Hortas](https://github.com/rubenhortas)
