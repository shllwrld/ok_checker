import argparse
import requests
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
        masked_name = soup.find('div', {'class': 'ext-registration_tx taCenter'})
        masked_email = soup.find('a', {'data-l': 't,email'})
        masked_phone = soup.find('a', {'data-l': 't,phone'})
        if masked_phone:
            masked_phone = masked_phone.get('data-post')
        if masked_email:
            masked_email = masked_email.get('data-post')
        if masked_name:
            masked_name = masked_name.get_text()
        return {
            'masked_name': masked_name,
            'masked_email': masked_email,
            'masked_phone': masked_phone,
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


def console_run():
    arg_parser = argparse.ArgumentParser(description='Simple checker for ok.ru partial private data disclosure')
    arg_parser.add_argument('login_data', help='known credential to check (email / phone number / username)')
    args = arg_parser.parse_args()
    login_data = args.login_data
    response = check_login(login_data)
    console_output(login_data, response)


if __name__ == '__main__':
    console_run()

