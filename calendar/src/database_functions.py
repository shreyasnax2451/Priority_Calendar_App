from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
import smtplib
import schedule
import time
from datetime import datetime, timedelta

engine = create_engine('sqlite:///calendar_tasks.db')
Base = declarative_base()
# Base.metadata.create_all(engine)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String, unique=False)
    start = Column(String, unique=False)
    end = Column(String, unique=False)
    priority = Column(String)
    is_completed = Column(Boolean, unique = False, default = True)

Session = sessionmaker(bind=engine)
session = Session()

def change_date(date, no_of_days):
    start_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    start_date = start_date + timedelta(days = no_of_days)
    return start_date.strftime('%Y-%m-%dT%H:%M:%S')

def get_tasks_data(key = 'incomplete'):
    if key == 'completed':
        task_query = session.query(Task).filter(Task.is_completed == True).all()
    else:
        task_query = session.query(Task).filter(Task.is_completed == False).all()
    tasks = []
    for obj in task_query:
        row = {
            'title':obj.task_name,
            'start':obj.start,
            'end':obj.end
        }
        if obj.priority == '1':
            row["color"] = "#FF6C6C"
        elif obj.priority == '2':
            row['color'] = "#FFA500"
        else:
            row['color'] = '#00FF00'

        tasks.append(row)
    session.close()
    return tasks

def add_task_data(task_data):
    """ Add a new task """
    new_user = Task(
        task_name=task_data['title'], 
        start=task_data['start'], 
        end = task_data['end'], 
        priority = task_data['priority'],
        is_completed = task_data['is_completed']
    )
    session.add(new_user)
    session.commit()
    session.close()
    return True

def edit_task(**task_data):
    """ Edit the priority of a Task"""
    task = session.query(Task).filter_by(task_name=task_data['task_name']).first()
    if task_data.get('priority'):
        task.priority = task_data['priority']
    elif task_data.get('is_completed'):
        task.is_completed = True
    session.commit()
    session.close()
    return True

def shift_task():
    email = 'Your_Email'
    password = 'Your_Password'

    tasks_data = session.query(Task).filter(Task.is_completed == False).all()
    task_titles = []
    for task in tasks_data:
        task.start = change_date(task.start, 1)
        task.end = change_date(task.end, 1)
        task_titles.append(task.task_name)
        session.commit()
    session.close()
        
    email_body = """Following Tasks Have been rescheduled to tomorrow!\nPlease see the calendar and try to complete.\n""" + '\n'.join(task_titles) + '\n' + 'Thanks!'

    with smtplib.SMTP(host = "smtp.gmail.com", port = "587") as connection:
        connection.starttls()
        connection.login(user = email, password = password)
        connection.sendmail(
            from_addr = email, 
            to_addrs = email, 
            msg = f"Subject:Important Update: Tasks Deadline Moved\n\n{email_body}"
        )

# schedule.every().day.at("00:00").do(shift_task)

# while True:
#     schedule.run_pending()
#     time.sleep(10)