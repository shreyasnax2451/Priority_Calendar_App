import streamlit as st
import datetime
from datetime import timedelta
from src.database_functions import add_task_data
from src.notifications import schedule_notifications
import re

st.set_page_config(page_title="Add Task")

st.title('Add Task')

start_date = datetime.datetime.now()
end_date = datetime.datetime.now()

selected_dates = st.date_input(
    "Select a date range",
    value=(start_date, end_date),
    min_value=datetime.date(2023, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)

time_range = st.slider(
    "Select time range",
    value=(datetime.time(8, 0), datetime.time(18, 0)),
    min_value=datetime.time(0, 0),
    max_value=datetime.time(23, 59),
    format="HH:mm",
    step = timedelta(minutes = 5)
)

add_task_ = st.text_input('Add Task')

emails = st.text_area("Enter invitees emails, separated by commas:")

st.write('The invitees will get the mail regarding the task')

priority_option = st.radio(
    "Select Priority..",
    key="priority",
    options=[":red[Priority 1]", ":orange[Priority 2]", ":green[Priority 3]"],
)
priority = re.search(r'\d+', priority_option).group(0)

alert = st.selectbox(
        "Alert Message..",
        ("At event's time", 
         '15 minutes before', 
         '30 minutes before',
         '45 minutes before',
         '1 hour before',
         '2 hours before',
         'Custom'),
        index=None
        )

if alert:
    if alert == 'Custom':
        col1, col2 = st.columns(2)
        with col1:
            alert_time = st.number_input("Enter alert time")
        with col2:
            alert_unit = st.selectbox('Minutes or Hours', ('minutes', 'hours'), index = None)
    elif 'event' in alert:
        alert_time = 0
        alert_unit = 'minutes'
    else:
        alert_time = int(alert.split(' ')[0])
        if 'minutes' in alert:
            alert_unit = 'minutes'
        elif 'hour' in alert or 'hours' in alert:
            alert_unit = 'hours'

    if alert_unit == 'hours':
        alert_time = alert_time*60

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
                "is_completed":False,
                "alert":alert_time,
                "emails":emails
        }
        task_id = add_task_data(data)
        if task_id:
            st.success("Task Added in Calendar!")
            data['id'] = task_id
            data['key'] = 'add'
            schedule_notifications(data)
        else:
            st.error('Task Not Added!')