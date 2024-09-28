import os
import re
import smtplib
import functools
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def send_email(email: str, html_content: str, subject: str, data: dict) -> bool:
    try:
        date, time = data['start'].split('T')
        placeholders = {
                'event_name':data['title'],
                'date':date,
                'time':time
        }
        partial_replacer = functools.partial(replace_placeholders, placeholders=placeholders)
        html_content = re.sub('{{(.*?)}}', partial_replacer, html_content)
        sender_email = os.environ["EMAIL_ADDRESS_SMPT"]
        recipient_email = email
        password = os.environ["PASSWORD_SMPT"]

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            logger.info("Reminder email sent successfully!")
        return True
    except Exception as e:
        logger.exception(e)

def replace_placeholders(match, placeholders):
    key = match.group(1)
    return placeholders.get(key, f'<{key} not found>')
