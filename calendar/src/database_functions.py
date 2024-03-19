from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///calendar_tasks.db')
Base = declarative_base()
# Base.metadata.create_all(engine)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=False)
    start = Column(String, unique=False)
    end = Column(String, unique=False)
    priority = Column(String)
    is_completed = Column(Boolean, unique = False, default = True)
    alert = Column(Integer, unique=False)

Session = sessionmaker(bind=engine)
session = Session()

def get_tasks_data(key = 'incomplete'):
    if key == 'completed':
        task_query = session.query(Task).filter(Task.is_completed == True).all()
    else:
        task_query = session.query(Task).filter(Task.is_completed == False).all()
    tasks = []
    for obj in task_query:
        row = {
            'title':obj.title,
            'start':obj.start,
            'end':obj.end,
            'alert':obj.alert
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
        title=task_data['title'], 
        start=task_data['start'], 
        end = task_data['end'], 
        priority = task_data['priority'],
        is_completed = task_data['is_completed'],
        alert = task_data['alert']
    )
    session.add(new_user)
    session.commit()
    session.close()
    return True

def edit_task(edit_params):
    """ Edit the priority of a Task"""
    task = session.query(Task).filter_by(title=edit_params['title']).first()
    if edit_params.get('priority'):
        task.priority = edit_params['priority']
    elif edit_params.get('is_completed'):
        task.is_completed = True
    else:
        task.start = edit_params['start']
        task.end = edit_params['end']
    session.commit()
    session.close()
    return True

def delete_task(delete_params):
    user_to_delete = session.query(Task).filter(Task.title == delete_params['title']).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
    session.close()
    return True

def change_date(date, no_of_days):
    start_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    start_date = start_date + timedelta(days = no_of_days)
    return start_date.strftime('%Y-%m-%dT%H:%M:%S')