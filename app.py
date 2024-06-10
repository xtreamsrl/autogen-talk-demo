import streamlit as st

from src.main import run_agents

st.title("Data Visualization Buddy")

with st.form(key='my_form'):
    dataset_link = st.text_input(label="Put Here The Dataset Link",
                                 value="https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv")
    query = st.text_input(label="What You Want To See?",
                          value="plot a visualization that tells us about the relationship between weight and horsepower.")

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.text(query)
    with st.spinner('Let me think...'):
        run_agents(dataset_link, query)

    st.image("groupchat/results.png")
