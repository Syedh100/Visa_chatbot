import streamlit as st
from ollama_chat import ask_ollama, check_ollama_status  # ✅ Uses your local Ollama model (llama3)

# ------------------- Streamlit Page Setup -------------------
st.set_page_config(page_title="Visit-Visa Eligibility Chatbot", page_icon="🧠", layout="centered")

st.title("🧠 AI-Powered Visit-Visa Eligibility Chatbot")

# Check Ollama connection status
ollama_connected = check_ollama_status()
if ollama_connected:
    st.success("✅ AI Assistant Connected - Ready to help with UK visa questions!")
else:
    st.error("⚠️ AI Assistant Offline - Please start Ollama with 'ollama serve' and ensure llama3 model is installed")

st.write("Hi! I'm your AI assistant for UK visa questions. I can help with eligibility, requirements, and application guidance. Ask me anything!")

# ------------------- Initialize Chat State -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "ai"  # Start with AI mode
if "context" not in st.session_state:
    st.session_state.context = ""

# ------------------- Display Chat History -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------- Chat Input -------------------
user_input = st.chat_input("Ask me anything about UK visas...")

# Display user message immediately
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Check for special commands
    if any(keyword in user_input.lower() for keyword in ["restart", "start over", "new chat", "clear"]):
        st.session_state.messages = []
        st.session_state.user_data = {}
        st.session_state.context = ""
        st.rerun()

    # Build context from conversation history
    context = st.session_state.context
    recent_messages = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
    
    # Create conversation context
    conversation_history = ""
    for msg in recent_messages:
        if msg["role"] == "user":
            conversation_history += f"User: {msg['content']}\n"
        else:
            conversation_history += f"Assistant: {msg['content']}\n"
    
    # Create intelligent prompt for Llama 3
    ai_prompt = f"""You are an expert UK visa consultant and helpful assistant. You provide accurate, helpful information about UK visa requirements, eligibility, and application processes.

CONVERSATION CONTEXT:
{conversation_history}

USER'S LATEST QUESTION: {user_input}

INSTRUCTIONS:
- Answer naturally and conversationally
- Provide accurate UK visa information
- If you need more details to give a complete answer, ask follow-up questions
- Be helpful, professional, and friendly
- If the user asks about visa requirements, gather key info like nationality, purpose of visit, duration
- Keep responses concise but informative (2-3 sentences max unless more detail is needed)
- If you're unsure about specific visa rules, suggest they check the official UK government website

Respond as a helpful UK visa consultant:"""

    # Get AI response
    with st.spinner("🤔 Thinking..."):
        try:
            bot_reply = ask_ollama(ai_prompt)
            if not bot_reply or bot_reply.strip() == "":
                bot_reply = "I'm sorry, I didn't get a response. Could you please rephrase your question?"
        except Exception as e:
            bot_reply = f"I'm having trouble connecting to my AI system. Please try again in a moment. Error: {str(e)}"

    # Update context with user data if mentioned
    user_data = st.session_state.user_data
    if "nationality" in user_input.lower() and any(country in user_input.lower() for country in ["american", "canadian", "australian", "indian", "chinese", "german", "french", "spanish", "italian", "brazilian", "mexican", "japanese", "korean", "thai", "vietnamese", "philippine", "nigerian", "south african", "egyptian"]):
        # Extract nationality from the conversation
        for country in ["american", "canadian", "australian", "indian", "chinese", "german", "french", "spanish", "italian", "brazilian", "mexican", "japanese", "korean", "thai", "vietnamese", "philippine", "nigerian", "south african", "egyptian"]:
            if country in user_input.lower():
                user_data["nationality"] = country.title()
                break
    
    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)