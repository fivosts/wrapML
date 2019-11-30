#!/usr/bin/env python
import smtplib, ssl, imaplib
from email.mime.text import MIMEText


port = 465
smtp_server = "smtp.gmail.com"
sender_email = "ml.framew@gmail.com" 
receiver_email = "fivos_ts@hotmail.com" 
password = "prscustom24"

def broadcast_error(reporting_module, error, sender = sender_email, password = "", receiver = receiver_email, request_reply = False):

	if password == "":
		assert False, "SMTP Server password for {} not specified!".format(sender_email)

	message = MIMEText("Error Reported:\n\n---------------------------------------\n{}\n---------------------------------------\n\nError reported by ML mail agent".format(error))
	message['Subject'] = "{} crashed!".format(reporting_module)
	message['From'] = sender
	message['To'] = receiver

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message.as_string())

	return

def receive_instruction():

	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(sender_email, password)
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.

	result, data = mail.search(None, "ALL")

	print(result)
	print(data)

	ids = data[0] # data is a list.
	print(ids)
	id_list = ids.split() # ids is a space separated string
	print(id_list)

	latest_email_id = id_list[-1] # get the latest

	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

	raw_email = data[0][1] # here's the body, which is raw text of the whole email
	# including headers and alternate payloads
	print(raw_email)

	return

body = "  File \"<stdin>\", line 1, in <module>\nFileNotFoundError: [Errno 2] No such file or directory: \'dimitroula.txt\'"

broadcast_error("Cluster classifier", body, password = "prscustom24")
# receive_instruction()