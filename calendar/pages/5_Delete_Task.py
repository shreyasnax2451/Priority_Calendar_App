from src.database_functions import get_tasks_data, delete_task
import streamlit as st
from src.notifications import schedule_notifications

st.set_page_config(page_title = "Delete Task")

st.title('Delete Task')

tasks_data = get_tasks_data()

tasks = (task['title'] for task in tasks_data)

selected_task = st.selectbox(
   "Which Task You want to delete?",
   tasks,
   index=None,
   placeholder="Select Task...",
)

delete_params = {}
for param in tasks_data:
    if param['title'] == selected_task:
        delete_params = param

if st.button('Delete this Task'):
    response = delete_task({
        'title':selected_task
    })
    if response:
        delete_params = delete_params | {
            'key':'delete'
        }
        schedule_notifications(delete_params)
        st.success("Task Deleted! Please check the calendar")
    else:
        st.error('Task Not Edited!')