import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def schedule_notifications(task_data):
    scheduler = BackgroundScheduler()
    reminder_time = datetime.strptime(task_data["start"], '%Y-%m-%dT%H:%M:%S') - timedelta(minutes=task_data['alert'])
    scheduler.add_job(send_email_notification, 'date', run_date=reminder_time, args=[task_data['title']])
    scheduler.start()
    jobs = scheduler.get_jobs()
    for job in jobs:
        print(f"Job: {job}")
        print(f"  Trigger: {job.trigger}")
        print(f"  Next Run Time: {job.next_run_time}")
        print(f"  Job Arguments: {job.args}")

def send_email_notification():
    with open('calendar/templates/email_template.html', 'r') as f:
        html_template = f.read()

    html_content = html_template.replace('[Event Name]', 'Task 1').replace('[Recipient Name]', 'Shreyas').replace('[date]', '2024-03-21').replace('[time]', '10:00 AM')

    sender_email = "shreyasnax2451@gmail.com"
    recipient_email = "shreyasnax2451@gmail.com"
    password = "rewcpxslqbfgajod"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Reminder: Incoming Task Alert"
    message["From"] = sender_email
    message["To"] = recipient_email

    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Reminder email sent successfully!")

def send_sms_notification():
    pass

# def notify_through_mail(title):
    # tasks_data = session.query(Task).filter(Task.is_completed == False).all()
    # task_titles = []
    # for task in tasks_data:
    #     task.start = change_date(task.start, 1)
    #     task.end = change_date(task.end, 1)
    #     task_titles.append(task.title)
    #     session.commit()
    # session.close()