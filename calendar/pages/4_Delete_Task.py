from src.database_functions import get_tasks_data, delete_task
import streamlit as st

tasks = (task['title'] for task in get_tasks_data())
selected_task = st.selectbox(
   "Which Task You want to delete?",
   tasks,
   index=None,
   placeholder="Select Task...",
)

if st.button('Delete this Task'):
    response = delete_task({
        'title':selected_task
    })
    if response:
        st.success("Task Deleted! Please check the calendar")
    else:
        st.error('Task Not Edited!')