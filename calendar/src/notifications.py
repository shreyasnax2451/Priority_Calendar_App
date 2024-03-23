from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from apscheduler.jobstores.memory import MemoryJobStore
from src.database_functions import session, Task
from src.helper import send_email
import concurrent.futures
import os
import re
import functools

scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
scheduler2 = BackgroundScheduler(jobstores={'default': MemoryJobStore()})

def replace_placeholders(match, placeholders):
        key = match.group(1)
        return placeholders.get(key, f'<{key} not found>')

def change_date(date, no_of_days):
    start_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    start_date = start_date + timedelta(days = no_of_days)
    return start_date.strftime('%Y-%m-%dT%H:%M:%S')

def schedule_notifications(task_data):
    reminder_time = datetime.strptime(task_data["start"], '%Y-%m-%dT%H:%M:%S') - timedelta(minutes=task_data['alert'])

    if task_data['key'] == 'add':
        task = session.query(Task).filter_by(id=task_data['id']).first()
        scheduler.add_job(send_alert_notification, 'date', run_date=reminder_time, args=[task_data])
        scheduler2.add_job(send_shifted_notification, 'date', run_date=datetime.strptime(task_data['end'], '%Y-%m-%dT%H:%M:%S'), args=[task_data])

    elif task_data['key'] == 'edit':
        task = session.query(Task).filter_by(id=task_data['id']).first()
        if scheduler.get_job(task.schedule_job_id):
            scheduler.remove_job(job_id = task.schedule_job_id)
        if scheduler2.get_job(task.schedule_job_id_2):
            scheduler2.remove_job(job_id = task.schedule_job_id_2)
        scheduler.add_job(send_alert_notification, 'date', run_date=reminder_time, args=[task_data])
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

def send_alert_notification(data):
    with open('calendar/templates/alert_email_template.html', 'r') as f:
        html_content = f.read()
    date, time = data['start'].split('T')
    placeholders = {
            'event_name':data['title'],
            'date':date,
            'time':time
    }
    partial_replacer = functools.partial(replace_placeholders, placeholders=placeholders)
    html_content = re.sub('{{(.*?)}}', partial_replacer, html_content)
    emails = [os.environ['EMAIL_ADDRESS_SMPT']]
    emails.extend(data['emails'].split(','))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(send_email, email, html_content, "Reminder: Incoming Task Alert") for email in emails]
        results = [f.result() for f in futures]    

def send_shifted_notification(data):
    task = session.query(Task).filter_by(id=data['id']).first()
    if not task.is_completed:
        with open('calendar/templates/deadline_email_template.html', 'r') as f:
            html_content = f.read()
        date, time = data['start'].split('T')
        placeholders = {
            'event_name':data['title'],
            'date':date,
            'time':time
        }
        partial_replacer = functools.partial(replace_placeholders, placeholders=placeholders)
        html_content = re.sub('{{(.*?)}}', partial_replacer, html_content)
        emails = [os.environ['EMAIL_ADDRESS_SMPT']]
        emails.extend(data['emails'].split(','))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(send_email, email, html_content, "Reminder: Task Deadline Crossed Alert") for email in emails]
            results = [f.result() for f in futures]  
        
            task.start = change_date(task.start, 1)
            task.end = change_date(task.end, 1)
            data['start'] = task.start
            data['end'] = task.end
            session.commit()
            session.close()
            schedule_notifications(data)

scheduler.start()
scheduler2.start()