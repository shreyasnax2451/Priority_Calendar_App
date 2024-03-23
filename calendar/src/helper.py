import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(email, html_content, subject):
    try:
        sender_email = os.environ['EMAIL_ADDRESS_SMPT']
        recipient_email = email
        password = os.environ['PASSWORD_SMPT']

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Reminder email sent successfully!")
    except Exception as e:
        print(e)
        print('Email Failed!')