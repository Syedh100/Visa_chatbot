import streamlit as st
import os
from ollama_chat import ask_ollama, check_ollama_status

# page setup
st.set_page_config(page_title="UK Visa Chatbot", page_icon="🧠", layout="centered")
st.title("UK Visa Chatbot")

# check ollama connection
if check_ollama_status():
    st.success("AI is connected and ready")
else:
    st.error("AI not connected. Run 'ollama serve' and make sure llama3 is installed")

st.write("Ask me anything about UK visas, like eligibility or requirements")

# sidebar stuff
with st.sidebar:
    st.write("Options")
    debug_mode = st.checkbox("Show debug info")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()

# store messages and user info
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "nationality": None,
        "purpose": None,
        "duration": None
    }

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# user input
user_input = st.chat_input("Type your question here")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # clear chat if asked
    if any(word in user_input.lower() for word in ["restart", "start over", "clear"]):
        st.session_state.clear()
        st.rerun()

    # extract info from what user says
    text = user_input.lower()

    # nationality
    countries = {
        "indian": "Indian", "pakistan": "Pakistani", "nigerian": "Nigerian",
        "bangladesh": "Bangladeshi", "american": "American", "canadian": "Canadian",
        "australian": "Australian", "chinese": "Chinese", "french": "French",
        "german": "German", "spanish": "Spanish"
    }
    for c in countries:
        if c in text:
            st.session_state.user_data["nationality"] = countries[c]
            break

    # purpose
    if "study" in text:
        st.session_state.user_data["purpose"] = "study"
    elif "work" in text:
        st.session_state.user_data["purpose"] = "work"
    elif any(word in text for word in ["visit", "tour", "holiday"]):
        st.session_state.user_data["purpose"] = "tourism"
    elif "business" in text:
        st.session_state.user_data["purpose"] = "business"
    elif "family" in text:
        st.session_state.user_data["purpose"] = "family"

    # duration
    if any(word in text for word in ["week", "month", "year", "day"]):
        st.session_state.user_data["duration"] = user_input

    # what info we know
    nationality = st.session_state.user_data["nationality"] or "Not mentioned"
    purpose = st.session_state.user_data["purpose"] or "Not mentioned"
    duration = st.session_state.user_data["duration"] or "Not mentioned"

    user_info = f"""
Nationality: {nationality}
Purpose: {purpose}
Duration: {duration}
    """

    # recent chat for context
    history = st.session_state.messages[-6:]
    conversation = ""
    for msg in history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # main prompt for AI
    prompt = f"""
You are a friendly UK visa assistant.
Use this info to answer questions and give advice.

User info:
{user_info}

Conversation so far:
{conversation}

New message: {user_input}

If something is missing like nationality, purpose, or duration, ask for it nicely.
Keep replies short, clear, and friendly.
    """

    # get reply from AI
    with st.spinner("Thinking..."):
        try:
            answer = ask_ollama(prompt, debug=debug_mode)
        except Exception as e:
            answer = f"Error: {str(e)}"

    # check if we are missing key info
    missing = []
    if not st.session_state.user_data["nationality"]:
        missing.append("your nationality")
    if not st.session_state.user_data["purpose"]:
        missing.append("the reason for your visit")
    if not st.session_state.user_data["duration"]:
        missing.append("how long you plan to stay")

    if missing and not any(word in text for word in ["nationality", "country", "stay", "visit"]):
        follow_up = f"Before I can give you proper advice, could you tell me {', and '.join(missing)}?"
        answer += f"\n\n{follow_up}"

    # show answer
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)