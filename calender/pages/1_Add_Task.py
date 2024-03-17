import streamlit as st
import datetime
from src.database_functions import add_task_data

st.set_page_config(page_title="Add Task")

st.title('Add Task')

start_date = datetime.datetime.now()
end_date = datetime.datetime.now()

selected_dates = st.date_input(
    "Select a date range",
    value=(start_date, end_date),
    min_value=datetime.date(2023, 1, 1),
    max_value=datetime.date(2024, 12, 31)
)

time_range = st.slider(
    "Select time range",
    value=(datetime.time(8, 0), datetime.time(18, 0)),
    min_value=datetime.time(0, 0),
    max_value=datetime.time(23, 59),
    format="HH:mm"
)

add_task_ = st.text_input('Add Task')
priority = st.selectbox(
        "Select Priority..",
        ('1', '2', '3'),
        index=None
        )

if st.button('Add The Task'):
    if len(selected_dates) == 1:
        start = end = selected_dates[0]
    else:
        start = selected_dates[0]
        end = selected_dates[1]
    
    if not add_task_:
        st.warning('Please Type Task Name',icon="⚠️")
    
    if not priority:
        st.warning('Please select Priority', icon="⚠️")

    if priority and add_task_:
        data = {
                "title": add_task_,
                "color": "#FFBD45",
                "start": start.strftime('%Y-%m-%d') + 'T' + time_range[0].strftime("%H:%M:%S"),
                "end": end.strftime('%Y-%m-%d') + 'T' + time_range[1].strftime("%H:%M:%S"),
                "priority": priority,
                "is_completed":False
        }
        if add_task_data(data):
            st.success("Task Added in Calendar!")
        else:
            st.error('Task Not Added!')