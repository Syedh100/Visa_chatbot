def remember_user_info(text, user_data):
    # nationality
    if "indian" in text or "india" in text:
        user_data["nationality"] = "Indian"
    elif "pakistan" in text:
        user_data["nationality"] = "Pakistani"
    elif "nigerian" in text:
        user_data["nationality"] = "Nigerian"
    elif "american" in text:
        user_data["nationality"] = "American"
    elif "canadian" in text:
        user_data["nationality"] = "Canadian"
    elif "chinese" in text:
        user_data["nationality"] = "Chinese"
    elif "australian" in text:
        user_data["nationality"] = "Australian"

    # purpose
    if "study" in text:
        user_data["purpose"] = "study"
    elif "work" in text:
        user_data["purpose"] = "work"
    elif "tour" in text or "visit" in text:
        user_data["purpose"] = "tourism"
    elif "business" in text:
        user_data["purpose"] = "business"
    elif "family" in text:
        user_data["purpose"] = "family"

    # duration
    if "week" in text or "month" in text:
        user_data["duration"] = text

def make_user_summary(user_data):
    nationality = user_data.get("nationality", "Not mentioned")
    purpose = user_data.get("purpose", "Not mentioned")
    duration = user_data.get("duration", "Not mentioned")
    
    return f"Nationality: {nationality}, Purpose: {purpose}, Duration: {duration}"

def make_conversation_history(messages):
    recent = messages[-4:]
    conv = ""
    for msg in recent:
        conv += f"{msg['role']}: {msg['content']}\n"
    return conv

def create_prompt(user_info, conv, user_input):
    prompt = f"""
You are a UK Government visa expert and immigration officer with extensive knowledge of UK visa policies, requirements, and procedures. Your role is to provide accurate, professional, and helpful guidance to users seeking UK visa information.

IMPORTANT CONVERSATION RULES:
- DO NOT introduce yourself on every reply
- DO NOT repeat phrases like "As a UK immigration expert…" more than once
- DO NOT repeat information that has already been given unless asked
- Maintain a natural conversation flow
- Keep responses short, friendly, and focused (2–4 sentences unless more detail is required)

OFFICIAL ROLE:
- UK Government Immigration Specialist
- Expert in all UK visa categories and requirements
- Authorized to provide official guidance on visa applications
- Committed to helping users understand UK immigration rules

CURRENT USER INFORMATION:
{user_info}

CONVERSATION HISTORY:
{conv}

USER'S CURRENT QUESTION:
{user_input}

YOUR RESPONSE REQUIREMENTS:
1. Answer as an official UK Government immigration expert
2. Provide accurate, current UK visa guidance
3. Ask follow-up questions when necessary to give the correct visa category or eligibility
4. Always remind users that official applications are made through GOV.UK — but ONLY once every few responses (not repeatedly)
5. Use correct visa terminology and simple explanations
6. Maintain a respectful, reassuring, and professional tone
7. If uncertain, request clarification rather than guessing

RESPOND TO THE USER NOW:
"""
    return prompt