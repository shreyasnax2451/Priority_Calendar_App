import streamlit as st
from src.database_functions import get_tasks_data, edit_task
import datetime

st.set_page_config(page_title = "Edited Tasks")

st.title('Edit Task')

tasks_data = get_tasks_data()

tasks = (task['title'] for task in tasks_data)
selected_task = st.selectbox(
   "Which Task You want to edit?",
   tasks,
   index=None,
   placeholder="Select Task...",
)

task_edit = st.selectbox(
   "How do you want to edit the task?",
   ('Change Timings of Task','Change Priority','Change Task Status to completed'),
   index=None,
   placeholder="Select Task...",
)

if task_edit == 'Change Priority':
    priority = st.selectbox(
    "Select Priority..",
    ('1', '2', '3'),
    index=None
    )
    is_completed = False
    edit_params = {
        'priority':priority,
        'is_completed':is_completed
    }
elif task_edit == 'Change Timings of Task':
    start, end, alert = [(task['start'], task['end'], task['alert']) for task in tasks_data if task['title'] == selected_task][0]

    start_date = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')

    edited_dates = st.date_input(
        "Select a date range",
        value=(start_date, end_date),
        min_value=datetime.date(2023, 1, 1),
        max_value=datetime.date(2024, 12, 31)
    )

    edited_time_range = st.slider(
        "Select time range",
        value=(start_date.time(), end_date.time()),
        min_value=datetime.time(0, 0),
        max_value=datetime.time(23, 59),
        format="HH:mm"
    )
    if len(edited_dates) == 1:
        start = end = edited_dates[0]
    else:
        start = edited_dates[0]
        end = edited_dates[1]

    edit_params = {
        'start' : start.strftime('%Y-%m-%d') + 'T' + edited_time_range[0].strftime("%H:%M:%S"),
        'end' : end.strftime('%Y-%m-%d') + 'T' + edited_time_range[1].strftime("%H:%M:%S"),
        'alert':alert
    }
else:
    edit_params = {
        'is_completed':True
    }

if st.button('Edit Task'):
    edit_params['title'] = selected_task
    edited = edit_task(edit_params)
    if edited:
        st.success("Task Edited in Calendar!")
    else:
        st.error('Task Not Edited!')