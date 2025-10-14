import requests
import json
import os

# talk to the ollama model
def ask_ollama(prompt, model="llama3", timeout=60, debug=False):
    """
    Send a message to the local Ollama model and get a reply.
    """

    # load the visa info if it exists
    data_path = os.path.join("Knowledge_base", "uk_visa_info.txt")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            visa_info = f.read()
    else:
        visa_info = "No visa information found."

    # build the full message for the model
    full_prompt = f"""
You are a UK visa assistant.
Use the info below to answer the user’s questions accurately.

UK Visa Knowledge:
{visa_info}

User Question:
{prompt}

Instructions:
- Keep answers short and clear.
- Be friendly and polite.
- If the question isn't about visas, let the user know.
    """

    # send request to ollama
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            },
            timeout=timeout,
            headers={'Content-Type': 'application/json'}
        )

        response.raise_for_status()

        reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        reply += data["response"]
                    if data.get("done", False):
                        break
                except:
                    continue

        if not reply.strip():
            return "Sorry, I didn’t get a proper response. Try asking again."
        if debug:
            reply += "\n\n[Debug: Model used = llama3]"
        return reply.strip()

    # handle errors
    except requests.exceptions.ConnectionError:
        return "Could not connect to Ollama. Make sure it’s running with 'ollama serve'."
    except requests.exceptions.Timeout:
        return "The request took too long. Try again with a shorter question."
    except Exception as e:
        return f"Error: {str(e)}"


# check if ollama is running
def check_ollama_status():
    try:
        res = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        return res.status_code == 200
    except:
        return False