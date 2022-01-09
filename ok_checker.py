#!/usr/bin/env python3
import argparse
import requests
import os
from bs4 import BeautifulSoup


OK_LOGIN_URL = \
    'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
OK_RECOVER_URL = \
    'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'


def check_login(login_data):
    session = requests.Session()
    session.get(f'{OK_LOGIN_URL}&st.email={login_data}')
    request = session.get(OK_RECOVER_URL)
    root_soup = BeautifulSoup(request.content, 'html.parser')
    soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
    if soup:
        account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
        masked_email = soup.find('button', {'data-l': 't,email'})
        masked_phone = soup.find('button', {'data-l': 't,phone'})
        if masked_phone:
            masked_phone = masked_phone.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if masked_email:
            masked_email = masked_email.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if account_info:
            masked_name = account_info.find('div', {'class': 'ext-registration_username_header'})
            if masked_name:
                masked_name = masked_name.get_text()
            account_info = account_info.findAll('div', {'class': 'lstp-t'})
            if account_info:
                profile_info = account_info[0].get_text()
                profile_registred = account_info[1].get_text()
            else:
                profile_info = None
                profile_registred = None
        else:
            return None

        return {
            'masked_name': masked_name,
            'masked_email': masked_email,
            'masked_phone': masked_phone,
            'profile_info': profile_info,
            'profile_registred': profile_registred,
        }

    if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
        return 'not associated'


def console_output(login_data, parsed_response):
    if parsed_response:
        if parsed_response == 'not associated':
            print(f'{login_data} not associated with ok.ru login')
        else:
            print(f'{login_data} associated with ok.ru login')
            for key, value in parsed_response.items():
                if value:
                    print(f'{key} - {value}')
    else:
        print('No fault, but server return unknown response')


def process_login(login_data):
    response = check_login(login_data)
    console_output(login_data, response)


def handle_file_input(filename):
    if os.path.isfile(filename):
        print(f"processing file {filename}...")
        with open(filename, "r") as f:
            logins = f.readlines()
        for login in logins:
            print("*" * 60)
            login = login.strip()
            process_login(login)
    else:
        print(f"file {filename} does not exist")


def console_run():
    arg_parser = argparse.ArgumentParser(description='Simple checker for ok.ru partial private data disclosure')
    arg_parser.add_argument('login_data', help='known credential to check (email / phone number / username)\
     or filepath (if option -f is set)')
    arg_parser.add_argument('-f', '--file', help='input file which contains credentials split by end of line',
                            action="store_true")
    args = arg_parser.parse_args()
    login_data = args.login_data
    if args.file:
        handle_file_input(login_data)
    else:
        process_login(login_data)


if __name__ == '__main__':
    console_run()

