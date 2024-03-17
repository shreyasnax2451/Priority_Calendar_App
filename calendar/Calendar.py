import streamlit as st
from streamlit_calendar import calendar
import datetime
from src.database_functions import get_tasks_data

st.set_page_config(page_title="Calendar App")

st.title('Calendar App')

events = get_tasks_data()

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": [],
    "selectable": "true",
}

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "list"
    ),
)

if mode == "daygrid":
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": datetime.datetime.today().strftime('%Y-%m-%d'),
        "initialView": "dayGridMonth",
    }
elif mode == "timegrid":
    calendar_options = {
        **calendar_options,
        "initialView": "timeGridWeek",
    }
elif mode == "timeline":
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "timelineDay,timelineWeek,timelineMonth",
        },
        "initialDate": datetime.datetime.today().strftime('%Y-%m-%d'),
        "initialView": "timelineMonth",
    }
elif mode == "list":
    calendar_options = {
        **calendar_options,
        "initialDate": datetime.datetime.today().strftime('%Y-%m-%d'),
        "initialView": "listMonth",
    }

state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.6;
    }
    .fc-event-time {
        font-style: courier-new;
    }
    .fc-event-title {
        font-weight: 600;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)