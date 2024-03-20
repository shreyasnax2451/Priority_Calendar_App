import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from apscheduler.jobstores.memory import MemoryJobStore
from src.database_functions import session, Task

scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
scheduler2 = BackgroundScheduler(jobstores={'default': MemoryJobStore()})

def change_date(date, no_of_days):
    start_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    start_date = start_date + timedelta(days = no_of_days)
    return start_date.strftime('%Y-%m-%dT%H:%M:%S')

def schedule_notifications(task_data):
    reminder_time = datetime.strptime(task_data["start"], '%Y-%m-%dT%H:%M:%S') - timedelta(minutes=task_data['alert'])
    if task_data['key'] == 'add':
        task = session.query(Task).filter_by(id=task_data['id']).first()
        scheduler.add_job(send_email_notification, 'date', run_date=reminder_time, args=[task_data])
        scheduler2.add_job(send_shifted_notification, 'date', run_date=datetime.strptime(task_data['end'], '%Y-%m-%dT%H:%M:%S'), args=[task_data])
    elif task_data['key'] == 'edit':
        task = session.query(Task).filter_by(id=task_data['id']).first()
        if scheduler.get_job(task.schedule_job_id):
            scheduler.remove_job(job_id = task.schedule_job_id)
        if scheduler2.get_job(task.schedule_job_id_2):
            scheduler2.remove_job(job_id = task.schedule_job_id_2)
        scheduler.add_job(send_email_notification, 'date', run_date=reminder_time, args=[task_data])
        scheduler2.add_job(send_shifted_notification, 'date', run_date=datetime.strptime(task_data['end'], '%Y-%m-%dT%H:%M:%S'), args=[task_data])
    elif task_data['key'] == 'delete':
        if scheduler.get_job(task_data['schedule_job_id']):
            scheduler.remove_job(job_id = task_data['schedule_job_id'])
        if scheduler2.get_job(task_data['schedule_job_id_2']):
            scheduler2.remove_job(job_id = task_data['schedule_job_id_2'])
    if task_data['key'] != 'delete':
        for job in scheduler.get_jobs():
            if job.args[0]['title'] == task.title:
                task.schedule_job_id = job.id
                session.commit()
                break

        for job2 in scheduler2.get_jobs():
            if job2.args[0]['title'] == task.title:
                task.schedule_job_id_2 = job2.id
                session.commit()
                break
        session.close()

def send_email_notification(data):
    with open('calendar/templates/email_template.html', 'r') as f:
        html_template = f.read()
    date, time = data['start'].split('T')
    html_content = html_template.replace('[Event Name]', data['title']).replace('[Recipient Name]', 'Shreyas').replace('[date]', date).replace('[time]', time)
    emails = data['emails'].split(',')
    try:
        for email in emails:
            sender_email = "shreyasnax2451@gmail.com"
            recipient_email = email
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
    except Exception as e:
        print(e)
        print('Email Failed!')

def send_shifted_notification(data):
    task = session.query(Task).filter_by(id=data['id']).first()
    if not task.is_completed:
        with open('calendar/templates/shifted_notify_calendar.html', 'r') as f:
            html_template = f.read()
        date, time = data['start'].split('T')
        html_content = html_template.replace('[Event Name]', data['title']).replace('[Recipient Name]', 'Shreyas').replace('[date]', date).replace('[time]', time)
        emails = data['emails'].split(',')
        try:
            for email in emails:
                sender_email = "shreyasnax2451@gmail.com"
                recipient_email = email
                password = "rewcpxslqbfgajod"

                message = MIMEMultipart("alternative")
                message["Subject"] = "Reminder: Task Deadline Crossed Alert"
                message["From"] = sender_email
                message["To"] = recipient_email

                html_part = MIMEText(html_content, "html")
                message.attach(html_part)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, recipient_email, message.as_string())
                    print("Reminder email sent successfully!")

                task.start = change_date(task.start, 1)
                task.end = change_date(task.end, 1)
                data['start'] = task.start
                data['end'] = task.end
                session.commit()
                session.close()
                schedule_notifications(data)
        except Exception as e:
            print(e)
            print('Email Failed!')

scheduler.start()
scheduler2.start()