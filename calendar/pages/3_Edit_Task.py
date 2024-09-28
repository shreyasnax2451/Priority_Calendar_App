import streamlit as st
from src.database_functions import get_tasks_data, edit_task
import datetime
from datetime import timedelta
from src.notifications import schedule_notifications

st.set_page_config(page_title="Edited Tasks")

st.title("Edit Task")

tasks_data = get_tasks_data()

tasks = (task["title"] for task in tasks_data)
selected_task = st.selectbox(
    "Which Task You want to edit?",
    tasks,
    index=None,
    placeholder="Select Task...",
)

edit_params = {}
for param in tasks_data:
    if param["title"] == selected_task:
        edit_params = param

task_edit = st.selectbox(
    "How do you want to edit the task?",
    (
        "Change Timings of Task",
        "Change Priority",
        "Change Task Status to completed",
        "Change Invitees",
    ),
    index=None,
    placeholder="Select Task...",
)

if task_edit == "Change Priority":
    priority = st.selectbox("Select Priority..", ("1", "2", "3"), index=None)
    edit_params = edit_params | {"priority": priority, "is_completed": False}
elif task_edit == "Change Timings of Task":
    start, end = [
        (task["start"], task["end"])
        for task in tasks_data
        if task["title"] == selected_task
    ][0]

    start_date = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

    edited_dates = st.date_input(
        "Select a date range",
        value=(start_date, end_date),
        min_value=datetime.date(2023, 1, 1),
        max_value=datetime.date(2030, 12, 31),
    )

    edited_time_range = st.slider(
        "Select time range",
        value=(start_date.time(), end_date.time()),
        min_value=datetime.time(0, 0),
        max_value=datetime.time(23, 59),
        format="HH:mm",
        step=timedelta(minutes=2),
    )
    if len(edited_dates) == 1:
        start = end = edited_dates[0]
    else:
        start = edited_dates[0]
        end = edited_dates[1]

    edit_params = edit_params | {
        "start": start.strftime("%Y-%m-%d")
        + "T"
        + edited_time_range[0].strftime("%H:%M:%S"),
        "end": end.strftime("%Y-%m-%d")
        + "T"
        + edited_time_range[1].strftime("%H:%M:%S"),
    }

elif task_edit == "Change Invitees":
    new_emails = st.text_input("Edit Invitees", value=edit_params["emails"])
    edit_params = edit_params | {"emails": new_emails, "emails_change": True}

elif task_edit == "Change Task Status to completed":
    edit_params = edit_params | {"is_completed": True}

if st.button("Edit Task"):
    edited_id = edit_task(edit_params)
    if edited_id:
        edit_params["id"] = edited_id
        edit_params["key"] = "edit"
        if task_edit != "Change Priority" and edit_params["alert"] != None:
            schedule_notifications(edit_params)
        st.success("Task Edited in Calendar!")
    else:
        st.error("Task Not Edited!")
