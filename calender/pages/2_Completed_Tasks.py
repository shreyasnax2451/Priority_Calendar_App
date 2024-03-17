import streamlit as st
from streamlit_calendar import calendar as cal
import datetime
from src.database_functions import get_tasks_data

st.set_page_config(page_title="Completed Tasks")

st.title('Completed Tasks')

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": [],
    "selectable": "true",
}

cal_options = {
    **calendar_options,
    "initialDate": datetime.datetime.today().strftime('%Y-%m-%d'),
    "initialView": "listMonth",
}

completed_events = get_tasks_data(key = 'completed')
state = cal(
    events = st.session_state.get("events", completed_events),
    options = cal_options,
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
    """
)