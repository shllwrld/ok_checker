usage: ok_parser.py [-h] [-f] login_data

Simple checker for ok.ru partial private data disclosure

positional arguments:

    login_data    known credential to check (email / phone number / username)\
     or filepath (if option -f is set)

optional arguments:

    -h, --help    show this help message and exit 

    -f, --file    input file which contains credentials split by end of line

Requirements:
  - python3.6+
  - bs4
