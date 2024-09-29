import os
import streamlit as st

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

from common.constants import RED, ORANGE, GREEN

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "calendar_tasks.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)

Base = declarative_base()
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=False)
    start = Column(String, unique=False)
    end = Column(String, unique=False)
    priority = Column(String)
    is_completed = Column(Boolean, unique=False, default=True)
    alert = Column(Integer, unique=False)
    schedule_job_id = Column(String, unique=False)
    schedule_job_id_2 = Column(String, unique=False)
    emails = Column(String, unique=False)


Session = sessionmaker(bind=engine)
session = Session()


def get_tasks_data(key="incomplete"):
    """Get the tasks data"""
    task_query = (
        session.query(Task).filter(Task.is_completed == (key == "completed")).all()
    )
    tasks = []
    for obj in task_query:
        row = {
            "title": obj.title,
            "start": obj.start,
            "end": obj.end,
            "alert": obj.alert,
            "schedule_job_id": obj.schedule_job_id,
            "schedule_job_id_2": obj.schedule_job_id_2,
            "emails": obj.emails,
            "priority": obj.priority,
            "is_completed": obj.is_completed,
        }
        if obj.priority == "1":
            row["color"] = RED
        elif obj.priority == "2":
            row["color"] = ORANGE
        else:
            row["color"] = GREEN

        tasks.append(row)
    session.close()
    return tasks


def add_task_data(task_data: dict):
    """Add a new task"""
    active_task_exists = (
        session.query(Task)
        .filter_by(title=task_data["title"], is_completed=False)
        .all()
    )
    if active_task_exists:
        st.error(f"Task already exists with name {task_data['title']}")
        return

    new_task = Task(
        title=task_data["title"],
        start=task_data["start"],
        end=task_data["end"],
        priority=task_data["priority"],
        is_completed=task_data["is_completed"],
        alert=task_data["alert"],
        emails=task_data["emails"],
    )
    session.add(new_task)
    session.commit()
    task_id = new_task.id
    session.close()
    return task_id


def edit_task(edit_params: dict):
    """Edit the timings, priority, status or invitees of a Task"""
    task = (
        session.query(Task)
        .filter_by(title=edit_params["title"], is_completed=False)
        .first()
    )

    if task:
        task.priority = edit_params["priority"]
        task.is_completed = edit_params["is_completed"]
        task.emails = edit_params["emails"]
        task.start = edit_params["start"]
        task.end = edit_params["end"]
        session.commit()
        task_id = task.id
        session.close()
        return task_id


def delete_task(delete_params: dict) -> bool:
    """Delete a Task"""
    task_to_delete = (
        session.query(Task)
        .filter_by(title=delete_params["title"], is_completed=False)
        .first()
    )
    if task_to_delete:
        session.delete(task_to_delete)
        session.commit()
    session.close()
    return True
