import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests import post
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime
from configparser import ConfigParser, NoOptionError, NoSectionError

INI_FILE = 'fox.ini'

def send_email(subject, body, config):
    try:
        sender = config.get('email', 'sender')
        receiver = config.get('email', 'receiver')
        smtp_server = config.get('email', 'smtp_server')
        smtp_port = int(config.get('email', 'smtp_port'))
        smtp_password = config.get('email', 'smtp_password')

        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Cc'] = sender
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, smtp_password)
            recipients = [receiver, sender]
            server.sendmail(sender, recipients, message.as_string())

    except NoSectionError as e:
        print(f'[{e.section}] section not found in {INI_FILE}')
        sys.exit(1)
    except NoOptionError as e:
        print(f'{e.section}.{e.option} key not found in {INI_FILE}')
        sys.exit(1)


def main():

    try:
        config = ConfigParser()
        config.read(INI_FILE)
    except FileNotFoundError:
        print('Config file not found')
        sys.exit(1)

    try:
        url = config.get('tracking', 'url')

        data = {
            'action': 'tracking',
            'n': config.get('tracking', 'num')
        }

        response = post(url, data=data)

        time_format = '%Y-%m-%d %H:%M:%S %Z%z'
        now_utc = datetime.now(timezone('UTC'))
        moscow_tz = timezone('Europe/Moscow')
        now_moscow = now_utc.astimezone(moscow_tz)
        moscow_timestamp = now_moscow.strftime(time_format)

        if response.status_code == 200:
            last_written_value = config.get('updated', 'timestamp')

            soup = BeautifulSoup(response.content, 'html.parser')
            last_tr = soup.find_all('tr')[-1]

            first_td_value = last_tr.find_all('td')[0].get_text(strip=True)
            if first_td_value != last_written_value:
                td_tags = last_tr.find_all('td')

                data_updated_at = td_tags[0].get_text(strip=True)
                data_state = td_tags[1].get_text(strip=True)
                data_description = td_tags[2].get_text(strip=True)

                email_body = f'''
                Мой робот заметил, что заявление было:

                обновлено: {data_updated_at}
                новый статус: {data_state}
                расшифровка: {data_description}
                '''

                send_email('Fox-express notification', email_body, config)

                config.set('updated', 'timestamp', first_td_value)
                with open(INI_FILE, 'w') as file:
                    config.write(file)

                print(f'{moscow_timestamp}\tEmail was sent')
            else:
                print(f'{moscow_timestamp}\tNothing new is here')
        else:
            error = f'{moscow_timestamp}\tFailed to fetch data:{response.status_code}'
            send_email('Fox-express error', error, config)
            print(error)
    except NoSectionError as e:
        print(f'[{e.section}] section not found in {INI_FILE}')
        sys.exit(1)
    except NoOptionError as e:
        print(f'{e.section}.{e.option} key not found in {INI_FILE}')
        sys.exit(1)

if __name__ == '__main__':
    main()
