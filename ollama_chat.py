import requests
import json
import os

def ask_ollama(prompt, model="llama3", timeout=60):
    """
    Sends a message to the local Ollama model and returns the model's reply as plain text.
    
    Args:
        prompt (str): The message to send to the AI model
        model (str): The model name (default: "llama3")
        timeout (int): Request timeout in seconds (default: 60)
    
    Returns:
        str: The AI model's response or an error message
    """
    try:
        # ------------------ Load UK Visa Knowledge ------------------
        knowledge_path = os.path.join("knowledge_base", "uk_visa_info.txt")
        if os.path.exists(knowledge_path):
            with open(knowledge_path, "r") as f:
                visa_knowledge = f.read()
        else:
            visa_knowledge = "No UK visa knowledge base found."

        # ------------------ Build Full Prompt ------------------
        full_prompt = f"""
You are an expert UK visa consultant. Use the following official UK visa information to answer user questions accurately.

UK VISA KNOWLEDGE:
{visa_knowledge}

USER QUESTION:
{prompt}

Instructions:
- Only use information from the UK visa knowledge section when applicable.
- If unsure, ask for clarification.
- Keep answers clear, concise, and friendly.
- If the user's question doesn't relate to visas, politely redirect them.
"""

        # ------------------ Send Request to Ollama ------------------
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,  # Makes responses more natural
                    "top_p": 0.9,        # Controls diversity
                    "max_tokens": 500    # Limits response length
                }
            },
            timeout=timeout,
            headers={'Content-Type': 'application/json'}
        )
        
        response.raise_for_status()
        
        # ------------------ Parse Streaming Response ------------------
        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data_str = line.decode("utf-8")
                    data = json.loads(data_str)
                    
                    if "response" in data:
                        full_reply += data["response"]
                    
                    if data.get("done", False):
                        break
                        
                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue
        
        cleaned_reply = full_reply.strip()
        if not cleaned_reply:
            return "I'm sorry, I didn't receive a proper response. Could you please try asking your question again?"
        
        return cleaned_reply

    # ------------------ Error Handling ------------------
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to Ollama. Please make sure Ollama is running with 'ollama serve' and the llama3 model is installed with 'ollama pull llama3'."
    
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. The AI model is taking too long to respond. Please try a shorter question."
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error connecting to Ollama: {str(e)}"
    
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

def check_ollama_status():
    """
    Check if Ollama is running and accessible.
    
    Returns:
        bool: True if Ollama is accessible, False otherwise
    """
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False