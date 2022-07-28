from os.path import exists
from os import uname
import argparse
from pathlib import Path
import requests
import smtplib
import ssl
from email.message import EmailMessage


class ZeroX():
    parser = argparse.ArgumentParser(
        prog=' oxo ',
        description='A simple tool to upload video and download video in 0x0.st ',
    )

    parser.add_argument(
        '-init', help='[ !!Note ] First command to run which is used to setup the program'
    )

    parser.add_argument(
        '-file', help=' [ Upload ] Take url location of video and give output as 0x0.st link '
    )
    parser.add_argument(
        '-password', help='[Setup password ] Take password and save it in a safe location'
    )
    parser.add_argument(
        '-mail', nargs=2, help='[ Send video url to email ] '
    )
    args = parser.parse_args()

    def __init__(self):
        pass

    def _init(self):
        try:

            user_name = uname().nodename  # get the linux username
            try:
                _path = Path(f'/home/{user_name}/.oxo')
                if exists(_path):
                    print("Already Initialized")
                else:
                    file = open(f'/home/{user_name}/.oxo', 'w')
                    file.write("")
                    file.close()
                    print("Scucessfull initialized the program")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def upload(self, _pa_th):
        if _pa_th:

            files = {
                'file': open(_pa_th, 'rb')
            }
            response = requests.post('https://0x0.st', files=files)
            res_ = response.content.decode('utf-8')
            w_link = open(f'/home/{uname().nodename}/.oxo', 'w')
            w_link.write(res_)
            print(f'Your file was uploaded sucessfully [link] : {res_}')

        else:
            print(_pa_th, "is not a valid path")

    def setup_pass(self):
        p_file = open(f'/home/{uname().nodename}/.pass', 'w')
        usr_inp = str(self.args.password)
        p_file.write(usr_inp)

    def email(self):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = ZeroX.args.mail[0]
        password_ = open(f'/home/{uname().nodename}/.pass', 'r')
        password = password_.read()
        to_Send = ZeroX.args.mail[1]
        context = ssl.create_default_context()
        msg = EmailMessage()
        msg['Subject'] = "Your video link"
        msg['From'] = sender_email
        msg['To'] = to_Send
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            file = open(f'/home/{uname().nodename}/.oxo', 'r')

            _message = file.read()
            msg.set_content(_message)
            server.send_message(msg)
            print("Scucessfully sended the video link to your mail")
        except Exception as e:
            print(e)
        finally:
            server.quit()


run = ZeroX()


if run.args.init == "start":
    run._init()

if run.args.file:
    run.upload(run.args.file)
    print(
        "[!!Note ] You can send the video of link to your mail if you want by using command : python main.py -mail {yourmail} {to_send_email}")

if run.args.password:
    run.setup_pass()
    pass
if run.args.mail:
    print(
        """
        [!! Note] To use this feature you need to Create App Password in google
        and use that app password by running python3 main.py - password {generated_password}]
        [!! Tourtrail] link: https://exerror.com/smtplib-smtpauthenticationerror-username-and-password-not-accepted

        """)
    run.email()
