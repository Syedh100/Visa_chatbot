import requests
import json
import os

def ask_ollama(prompt, model="llama3", timeout=60):
    # load visa info
    file_path = os.path.join("knowledge_base", "uk_visa_info.txt")
    visa_info = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            visa_info = f.read()
    else:
        visa_info = "No visa info found"

    # make prompt
    full_prompt = f"""
    You help with UK visas. Use this info:
    
    {visa_info}
    
    Question: {prompt}
    
    Answer clearly.
    """

    try:
        # send to ollama
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            },
            timeout=timeout
        )
        
        response.raise_for_status()
        
        # get response
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

        if reply.strip():
            return reply.strip()
        else:
            return "No response from AI"

    except requests.exceptions.ConnectionError:
        return "Cannot connect to Ollama"

    except requests.exceptions.Timeout:
        return "Request timeout"

    except Exception as e:
        return f"Error: {str(e)}"

def check_ollama_status():
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False