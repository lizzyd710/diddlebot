"""
File diddlemail.py

Contains all the stuff you need to send an email as diddlebot, minus the credentials.
Password for the email is stored similar to the discord auth token, in a file called
email in the directory diddlebot runs within.

:author Sam Kuzio
"""

import smtplib, ssl, os.path

CRED_FILE = "email"
PORT = 587
EMAIL = "diddlebot9000@gmail.com"
EMAIL_PASSWORD = None
SMTP_SERVER = "smtp.gmail.com"
CLUB_EMAIL = "drumline@rit.edu"


def load_creds():
    """
    Attempts to load email password.
    :return:
    """

    global EMAIL_PASSWORD

    try:
        with open('email', 'r') as email_file:
            EMAIL_PASSWORD = email_file.read().strip()
    except FileNotFoundError:
        EMAIL_PASSWORD = None
        print("No email file present - email functionality will not work. To fix this, ensure the email file exists in"
              " the current working directory with the email account password.")
        return

    if EMAIL_PASSWORD is None or EMAIL_PASSWORD == "":
        EMAIL_PASSWORD = None
        print("Warning: No password was found in the email file. Email functionality will not work!")
    else:
        print("Loaded email configuration")


def send_email_to_club(message, subject):
    """
    Sends a plain text email message to the club email account.
    :param message: The body text of the message
    :param subject: The subject line of the message
    :return: True iff the email was sent successfully, or if email is not configured. False if an error
             occurs when sending an email.
    """

    if EMAIL_PASSWORD is None:
        print("Warning: Cannot send email - no email password is loaded!")

        # This is not considered a failure, rather a misconfiguration. Notifying via logs is ok here.
        return True

    # as called for by the basic smtp protocol, append the subject line before the message
    message = "Subject: " + subject + "\n\n" + message

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, CLUB_EMAIL, message)
        return True
    except Exception as e:
        print(e)
        return False
