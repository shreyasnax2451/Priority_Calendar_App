import streamlit as st
from datetime import datetime

from common.constants import RED, ORANGE, GREEN
from src.database_functions import get_tasks_data

tasks = tasks_data = get_tasks_data()
st.header("Incomplete Tasks Overview")

if not tasks:
    st.write("Hurray! No Pending Tasks!")
else:
    for task in tasks:
        st.subheader(task["title"])
        with st.expander("Details"):
            st.write("Invitees: ", task["emails"])
            if task["color"] == RED:
                st.write("Priority: ", ":red[Priority 1]")
            elif task["color"] == ORANGE:
                st.write("Priority: ", ":orange[Priority 2]")
            elif task["color"] == GREEN:
                st.write("Priority: ", ":green[Priority 3]")

            st.write(
                "Start Time: ", datetime.strptime(task["start"], "%Y-%m-%dT%H:%M:%S")
            )
            st.write("End Time: ", datetime.strptime(task["end"], "%Y-%m-%dT%H:%M:%S"))
