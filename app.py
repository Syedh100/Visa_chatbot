import streamlit as st
import os
from ollama_chat import ask_ollama, check_ollama_status
from user_utils import remember_user_info, make_user_summary, make_conversation_history, create_prompt

st.set_page_config(page_title="UK Visa Chatbot", layout="centered")
st.title("UK Visa Chatbot")

st.write("Ask me about UK visas")

# check if ai works
if check_ollama_status():
    st.success("AI is working")
else:
    st.error("AI not working - start Ollama")

# sidebar
with st.sidebar:
    st.write("Options")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()

# setup
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# get input
user_input = st.chat_input("Type here")

if user_input:
    # add message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # restart check
    if "restart" in user_input.lower() or "clear" in user_input.lower():
        st.session_state.clear()
        st.rerun()

    # remember user info
    remember_user_info(user_input.lower(), st.session_state.user_data)
    
    # make context
    user_info = make_user_summary(st.session_state.user_data)
    conv = make_conversation_history(st.session_state.messages)
    prompt = create_prompt(user_info, conv, user_input)

    # get response
    with st.spinner("Typing..."):
        try:
            response = ask_ollama(prompt)
            if not response:
                response = "Sorry, no response. Try again."
        except Exception as e:
            response = f"Error: {str(e)}"

    # show response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)