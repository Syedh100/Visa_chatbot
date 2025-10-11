import requests
import json

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
        # Make request to Ollama API
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
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
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse streaming response
        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    # Decode the line and parse JSON
                    data_str = line.decode("utf-8")
                    data = json.loads(data_str)
                    
                    # Extract response text
                    if "response" in data:
                        full_reply += data["response"]
                    
                    # Check if this is the final response
                    if data.get("done", False):
                        break
                        
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
                except Exception:
                    # Skip any other parsing errors
                    continue
        
        # Clean up and return response
        cleaned_reply = full_reply.strip()
        if not cleaned_reply:
            return "I'm sorry, I didn't receive a proper response. Could you please try asking your question again?"
        
        return cleaned_reply

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