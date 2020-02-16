#!/usr/bin/env python
import smtplib, ssl, imaplib
from email.mime.text import MIMEText
import email
import subprocess
from datetime import datetime
import time

class mail_agent:

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "ml.framew@gmail.com" 
    receiver_email = "fivos_ts@hotmail.com" 
    password = "prscustom24"

    def __init__(this):
        return

    def broadcast_error(this, reporting_module, error, request_reply = False):

        if this.password == "":
            assert False, "SMTP Server password for {} not specified!".format(sender_email)

        message = this.generate_message(reporting_module, error)
        this.send_message(message)

        if request_reply:
            this.mailbox_check_wait(message)
            cmd = this.receive_instruction()
            this.execute_instructions(cmd)

        return

    def generate_message(this, rm, e):
        message = MIMEText("Error Reported:\n\n---------------------------------------\n{}\n---------------------------------------\n\nError reported by mail agent".format(e))
        message['Subject'] = "{}".format(rm)
        message['From'] = this.sender_email
        message['To'] = this.receiver_email
        message['Sent'] = str(datetime.now())
        return message

    def send_message(this, message):

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(this.smtp_server, this.port, context=context) as server:
            server.login(this.sender_email, this.password)
            server.sendmail(this.sender_email, this.receiver_email, message.as_string())
        return

    def receive_instruction(this):

        r, d = this.fetch_mail(encoding = "(UID BODY[TEXT])")
        msg = this.extract_email(d).as_string().split('\n')
        command = []

        for line in msg:
            if "$cmd" in line:
                command_str = ":".join(line.split(':')[1:])
                print(command_str)
                command = [x.split() for x in command_str.split(';') if x]
                print(command)
                break

        assert len(command) != 0, "Command field not extracted successfully!"
        return command

    def execute_instructions(this, cmd):

        for c in cmd:
            proc = subprocess.Popen(c, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            print(out.decode("utf-8"))
        return

    def extract_email(this, data):

        for response_part in data:
            if isinstance(response_part, tuple):
                return email.message_from_bytes(response_part[1])

        assert False, "Main email cannot be extracted: Wrong format!"

    def mailbox_check_wait(this, message):

        r, d = this.fetch_mail()
        msg = this.extract_email(d)

        while not (message['Subject'] in msg['Subject'] and message['To'] in msg['From']):     
            time.sleep(10)
            r, d = this.fetch_mail()
            msg = this.extract_email(d)
        return

    def fetch_mail(this, encoding = "(RFC822)"):

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(this.sender_email, this.password)
        mail.list()

        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox", readonly=True) # connect to inbox.
        result, data = mail.search(None, "ALL")
        id_list = data[0].split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        result, data = mail.fetch(latest_email_id, encoding) # fetch the email body (RFC822) for the given ID

        return result, data

mail = mail_agent()
# mail.broadcast_error("Training new script", "Something veeeerry bad happened!!!", request_reply = True)
mail.execute_instructions(mail.receive_instruction())
# mail.mailbox_check_wait("hello")
