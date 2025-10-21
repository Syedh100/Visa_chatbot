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
            "http://host.docker.internal:11434/api/generate",
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
        # fallback when ollama not available
        return get_fallback_response(prompt, visa_info)

    except requests.exceptions.Timeout:
        return get_fallback_response(prompt, visa_info)

    except Exception as e:
        return get_fallback_response(prompt, visa_info)

def get_fallback_response(prompt, visa_info):
    # simple keyword matching when ollama not available
    prompt_lower = prompt.lower()
    
    if "visitor" in prompt_lower or "tourist" in prompt_lower:
        return "For UK visitor visas, you typically need to apply online through GOV.UK. Requirements include a valid passport, proof of funds, and travel plans. Processing usually takes 3 weeks."
    
    elif "work" in prompt_lower:
        return "UK work visas have different requirements depending on your job. You'll need a job offer from a UK employer and meet specific criteria. Check GOV.UK for detailed requirements."
    
    elif "study" in prompt_lower:
        return "For UK student visas, you need an offer from a licensed UK educational institution, proof of English language ability, and financial support. Apply through GOV.UK."
    
    elif "family" in prompt_lower:
        return "UK family visas allow you to join family members in the UK. Requirements vary based on relationship and circumstances. Check the official GOV.UK website for specific details."
    
    elif "requirements" in prompt_lower:
        return "UK visa requirements vary by visa type. Generally you need a valid passport, application form, fees, and supporting documents. Visit GOV.UK for complete requirements."
    
    else:
        return f"Based on the available information: {visa_info[:200]}... For detailed help, please visit the official GOV.UK website or contact UK Visas and Immigration."

def check_ollama_status():
    try:
        response = requests.get("http://host.docker.internal:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False