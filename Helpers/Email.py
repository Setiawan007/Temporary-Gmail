from imap_tools import MailBox, AND
from dotenv import dotenv_values
import random
import datetime


class Email:

    def __init__(self):
        pass

    def Login(self):
        config = dotenv_values("./.env")
        mailbox = MailBox(
            host='imap.gmail.com',
            timeout=5,
        ).login(config.get("Email"), config.get("Password"))
        self.mailbox = mailbox
        self.config = config
        return mailbox

    def GetMessages(self, email):
        try:
            self.mailbox.idle.wait(timeout=3)
            data_msg = []
            for msg in self.mailbox.fetch(AND(to=email), reverse=True):
                data_msg.append({
                    'to': msg.to,
                    'uid': msg.uid,
                    'from': msg.from_,
                    'date': msg.date,
                    'subject': msg.subject,
                    'body': msg.text
                })

            if not data_msg:
                return {
                    'status': False,
                    'message': 'No messages appear',
                    'email': email,
                }
            else:
                return {
                    'status': True,
                    'message': 'Messages appear',
                    'email': email,
                    'data': data_msg
                }
        except Exception as e:
            print("[ {} ] Error : {}".format(datetime.datetime.now(), e))
            self.Login()
            return {
                'status': False,
                'message': str(e),
            }

    def delete_message(self, uid):
        try:
            self.mailbox.delete(uid)
            return True
        except Exception as e:
            print(e)
            return False

    def read_by(self, string_data, email):
        data_msg = []
        for msg in self.mailbox.fetch(AND(to=email, body=string_data), reverse=True):
            data_msg.append({
                'to': msg.to,
                'uid': msg.uid,
                'from': msg.from_,
                'date': msg.date,
                'subject': msg.subject,
                'body': msg.text
            })

        if not data_msg:
            return {
                'status': False,
                'message': 'No messages appear',
                'email': email,
            }
        else:
            return {
                'status': True,
                'message': 'Messages appear',
                'email': email,
                'data': data_msg
            }

    def generate_email(self, type):
        g = lambda e: (
            f"{''.join(p + t for p, t in zip(((['', '.'][s >> i & 1] for i in range(len(e) - 1, -1, -1))), e))}@gmail.com"
            for s in range(2 ** (len(e) - 1)))

        if type == "dot":
            data_rand = random.choice(list(g(
                self.config.get("Email").split("@")[0]
            )))
            return {
                'status': True,
                'email': data_rand,
                'mailbox': '/read/' + data_rand
            }

        elif type == "dotplus":
            data_rand = random.choice(list(g(
                self.config.get("Email").split("@")[0]
            ))).split('@')[0] + '+' + str(
                random.randint(1, 99)) + '@gmail.com'
            return {
                'status': True,
                'email': data_rand,
                'mailbox': '/read/' + data_rand
            }
