import streamlit as st
import os
from ollama_chat import ask_ollama, check_ollama_status  # Connects to Ollama

# ------------------- Streamlit Page Setup -------------------
st.set_page_config(page_title="Visit-Visa Eligibility Chatbot", page_icon="🧠", layout="centered")
st.title("🧠 AI-Powered Visit-Visa Eligibility Chatbot")

# ------------------- Ollama Connection Check -------------------
ollama_connected = check_ollama_status()
if ollama_connected:
    st.success("✅ AI Assistant Connected - Ready to help with UK visa questions!")
else:
    st.error("⚠️ AI Assistant Offline - Please start Ollama with 'ollama serve' and ensure llama3 model is installed")

st.write("Hi! I'm your AI assistant for UK visa questions. I can help with eligibility, requirements, and application guidance. Ask me anything!")

# ------------------- Initialize Session State -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "ai"
if "context" not in st.session_state:
    st.session_state.context = ""

# ------------------- Display Chat History -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------- Chat Input -------------------
user_input = st.chat_input("Ask me anything about UK visas...")

# ------------------- Handle User Input -------------------
if user_input:
    # Display user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Handle restart / clear chat
    if any(keyword in user_input.lower() for keyword in ["restart", "start over", "new chat", "clear"]):
        st.session_state.messages = []
        st.session_state.user_data = {}
        st.session_state.context = ""
        st.rerun()

    # ------------------- Build Conversation History -------------------
    recent_messages = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
    conversation_history = ""
    for msg in recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_history += f"{role}: {msg['content']}\n"

    # ------------------- Build AI Prompt -------------------
    ai_prompt = f"""
You are an expert UK visa consultant and helpful assistant. 
You provide accurate, helpful information about UK visa requirements, eligibility, and application processes.

CONVERSATION CONTEXT:
{conversation_history}

USER'S QUESTION: {user_input}

INSTRUCTIONS:
- Provide accurate UK visa information based on your knowledge.
- If you need more details to give a complete answer, ask follow-up questions.
- Be professional, friendly, and clear.
- Keep answers short (2–4 sentences) unless detail is needed.
- If unsure about specific rules, suggest visiting the official GOV.UK site.
"""

    # ------------------- Generate AI Response -------------------
    with st.spinner("🤔 Thinking..."):
        try:
            bot_reply = ask_ollama(ai_prompt)
            if not bot_reply or bot_reply.strip() == "":
                bot_reply = "I'm sorry, I didn’t get a response. Could you rephrase your question?"
        except Exception as e:
            bot_reply = f"⚠️ I'm having trouble connecting to my AI system. Error: {str(e)}"

    # ------------------- Store and Display AI Response -------------------
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)