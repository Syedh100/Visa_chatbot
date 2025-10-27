# 🇬🇧 UK Visa Chatbot

This is a simple AI chatbot that helps users with UK visa questions.  
It uses **Streamlit** for the web interface and **Ollama (Llama 3)** for local AI responses.

---

## 💡 What It Does
- Lets users chat and ask visa-related questions  
- Runs fully on your computer (no API keys needed)  
- Works through Docker or directly with Python  

---

## ⚙️ How to Run (Easiest Way — Docker)

### Step 1: Install Docker Desktop  
Make sure you have Docker Desktop installed and running.  
Download: https://www.docker.com/products/docker-desktop

### Step 2: Clone this project  
Open your terminal and run:
```bash
git clone https://github.com/Syedh100/Visa_chatbot.git
cd Visa_chatbot
```

### Step 3: Start everything  
Run this command:
```bash
bash start_chatbot.sh
```

This will:  
1. Start **Ollama** (the AI backend)  
2. Download the **Llama 3** model (if not already installed)  
3. Build and run the chatbot automatically  

### Step 4: Open the chatbot  
Once it’s done, open your browser and visit:  
http://localhost:8501

---

## 🧩 Optional: Run Without Docker
If you prefer running it locally without Docker:
```bash
pip install -r requirements.txt
streamlit run app.py
```

> Make sure **Ollama** is installed and running on your system first (`ollama serve`, then `ollama pull llama3`).

---

## 🧠 Notes  
- This project runs entirely **offline** — no external API keys needed.  
- The chatbot uses **Llama 3** locally via Ollama.  
- You can modify `app.py` and `ollama_chat.py` to customize behavior or prompts.  

---

## 🧰 Tech Stack  
- **Python 3.10+**  
- **Streamlit**  
- **Docker**  
- **Ollama (Llama 3 model)**  
