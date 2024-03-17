import streamlit as st
from src.database_functions import get_tasks_data, edit_task

st.set_page_config(page_title = "Edited Tasks")

st.title('Edit Task')

tasks = (task['title'] for task in get_tasks_data())
option = st.selectbox(
   "Which Task You want to edit?",
   tasks,
   index=None,
   placeholder="Select Task...",
)

task_edit = st.selectbox(
   "How do you want to edit the task?",
   ('Change Priority','Change Task Status to completed'),
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
else:
    priority = None
    is_completed = True

if st.button('Edit Task'):
    edited = edit_task(task_name = option, priority = priority, is_completed = is_completed)
    if edited:
        st.success("Task Edited in Calendar!")
    else:
        st.error('Task Not Edited!')