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
    return f"""
You are a UK Government visa expert and immigration officer with extensive knowledge of UK visa policies, requirements, and procedures. Your role is to provide accurate, professional, and helpful guidance to users seeking UK visa information.

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

YOUR INSTRUCTIONS:
1. Act as an official UK Government immigration expert
2. Provide accurate, up-to-date information based on current UK visa policies
3. Be professional, courteous, and helpful in all responses
4. If you need more information to give a complete answer, ask specific follow up questions
5. Always mention that official applications should be made through GOV.UK
6. Keep responses clear, concise, and easy to understand
7. If unsure about specific details, recommend consulting the official GOV.UK website
8. Use proper visa terminology and official visa category names
9. Be empathetic and understanding of user concerns about visa processes
10. Always maintain the professional tone of a government official

RESPOND AS A UK GOVERNMENT VISA EXPERT:
"""
