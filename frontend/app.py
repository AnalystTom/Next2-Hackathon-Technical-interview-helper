import streamlit as st
import requests

st.title("Hackathon Helper")

# Initial hackathon inputs
objective = st.text_input("Hackathon Objective")
technologies = st.text_input("Technologies to Use (comma-separated)")
judging_criteria = st.text_input("Judging Criteria (comma-separated)")
team_size = st.number_input("Number of Team Members", min_value=1, step=1)

teammates = []
for i in range(team_size):
    name = st.text_input(f"Team Member {i+1} Name")
    skills = st.text_input(f"Team Member {i+1} Skills (comma-separated)")
    teammates.append({"name": name, "skills": skills.split(",")})

# Start conversation
if st.button("Start Brainstorming"):
    input_data = {
        "objective": objective,
        "technologies": technologies.split(","),
        "judging_criteria": judging_criteria.split(","),
        "teammates": teammates
    }

    response = requests.post("http://localhost:8000/start_conversation/", json=input_data)

    if response.status_code == 200:
        initial_plan = response.json()
        st.session_state['conversation_state'] = initial_plan['conversation_state']
        st.write(initial_plan['response'])
    else:
        st.error("Failed to start the conversation. Please try again.")


if 'conversation_state' in st.session_state:
    user_input = st.text_input("Your next input")

    if st.button("Continue"):
        conversation_state = st.session_state['conversation_state']
        response = requests.post("http://localhost:8000/continue_conversation/", json={
            "conversation_state": conversation_state,
            "user_input": user_input
        })

        if response.status_code == 200:
            continued_convo = response.json()
            st.session_state['conversation_state'] = continued_convo['conversation_state']
            st.write(continued_convo['response'])
        else:
            st.error("Failed to continue the conversation. Please try again.")
