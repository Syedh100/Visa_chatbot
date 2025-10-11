import streamlit as st

st.title("🌍 Visit-Visa Eligibility Chatbot")
st.write("Hello! This is your first Streamlit app. 🎉")

name = st.text_input("What is your name?")
if name:
    st.success(f"Welcome, {name}! You're officially ready to build amazing apps.")