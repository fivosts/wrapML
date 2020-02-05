#!/usr/bin/env python
import smtplib, ssl, imaplib
from email.mime.text import MIMEText
import email
import subprocess

class mail_agent:

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "ml.framew@gmail.com" 
    receiver_email = "fivos_ts@hotmail.com" 
    password = "prscustom24"

    def __init__(this):
        return

    def broadcast_error(this, reporting_module, error, sender = "ml.framew@gmail.com", receiver = "fivos_ts@hotmail.com", request_reply = False):

        if this.password == "":
            assert False, "SMTP Server password for {} not specified!".format(sender_email)

        message = MIMEText("Error Reported:\n\n---------------------------------------\n{}\n---------------------------------------\n\nError reported by ML mail agent".format(error))
        message['Subject'] = "{} crashed!".format(reporting_module)
        message['From'] = sender
        message['To'] = receiver

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(this.smtp_server, this.port, context=context) as server:
            print(this.sender_email)
            print(this.password)
            server.login(this.sender_email, this.password)
            server.sendmail(this.sender_email, this.receiver_email, message.as_string())

        return

    def receive_instruction(this):

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(this.sender_email, this.password)
        mail.list()

        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox", readonly=True) # connect to inbox.
        result, data = mail.search(None, "ALL")

        id_list = data[0].split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest

        result, data = mail.fetch(latest_email_id, "(UID BODY[TEXT])") # fetch the email body (RFC822) for the given ID

        command = ""
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                msg_list = msg.as_string().split('\n')
                for line in msg_list:
                	if "$cmd" in line:
                		command = line.split(':')[1]
                		break

        proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        out, err = proc.communicate()
        print(out.decode("utf-8"))
        return

mail = mail_agent()
# mail.broadcast_error("Random module", "Hello from the other side !")
mail.receive_instruction()