import streamlit as st
import os
from ollama_chat import ask_ollama, check_ollama_status

st.set_page_config(page_title="UK Visa Chatbot", page_icon="🧠", layout="centered")
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

    # remember stuff
    text = user_input.lower()
    data = st.session_state.user_data

    # nationality
    if "indian" in text or "india" in text:
        data["nationality"] = "Indian"
    elif "pakistan" in text:
        data["nationality"] = "Pakistani"
    elif "nigerian" in text:
        data["nationality"] = "Nigerian"
    elif "american" in text:
        data["nationality"] = "American"
    elif "canadian" in text:
        data["nationality"] = "Canadian"
    elif "chinese" in text:
        data["nationality"] = "Chinese"
    elif "australian" in text:
        data["nationality"] = "Australian"

    # purpose
    if "study" in text:
        data["purpose"] = "study"
    elif "work" in text:
        data["purpose"] = "work"
    elif "tour" in text or "visit" in text:
        data["purpose"] = "tourism"
    elif "business" in text:
        data["purpose"] = "business"
    elif "family" in text:
        data["purpose"] = "family"

    # duration
    if "week" in text or "month" in text:
        data["duration"] = user_input

    # make context
    nationality = data.get("nationality", "Not mentioned")
    purpose = data.get("purpose", "Not mentioned")
    duration = data.get("duration", "Not mentioned")

    user_info = f"Nationality: {nationality}, Purpose: {purpose}, Duration: {duration}"

    # get recent messages
    recent = st.session_state.messages[-4:]
    conv = ""
    for msg in recent:
        conv += f"{msg['role']}: {msg['content']}\n"

    # make prompt
    prompt = f"""
    You help with UK visas.
    
    User info: {user_info}
    
    Chat: {conv}
    
    Question: {user_input}
    
    Answer helpfully.
    """

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