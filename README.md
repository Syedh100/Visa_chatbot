UK Visa Chatbot

An AI-powered chatbot that helps users understand UK visa eligibility, requirements, and application steps.
Built with Streamlit (front end), Ollama + Llama 3 (local LLM), and a small GOV.UK scraper to keep facts grounded.

⸻

Features
	•	Conversational chat UI (Streamlit)
	•	Local LLM via Ollama (no API keys or cloud costs)
	•	Guided flow to collect key details (nationality, purpose, duration)
	•	Knowledge grounding from official GOV.UK pages
	•	One-command startup using Docker + start_chatbot.sh

⸻

Architecture 
	•	app.py – Streamlit UI + conversation flow (collects user details and builds prompts)
	•	ollama_chat.py – Thin wrapper that calls the local Ollama API (Llama 3)
	•	update_visa_data.py – Scrapes relevant GOV.UK pages and saves text under Knowledge_base/
	•	start_chatbot.sh – Automates Docker steps (start Ollama, pull model, build & run app)
	•	Dockerfile – Containerizes the Streamlit app
	•	Knowledge_base/uk_visa_info.txt – Scraped GOV.UK content used to ground answers

⸻

Quick Start (recommended)

Prereqs: Docker Desktop installed and running.

# clone and enter the project
git clone https://github.com/Syedh100/Visa_chatbot.git
cd Visa_chatbot

# run everything with one command
bash start_chatbot.sh

The script will:
	1.	Clean up any old containers
	2.	Start an Ollama container and expose port 11434
	3.	Pull the llama3 model if not present
	4.	Build the chatbot image
	5.	Launch the Streamlit app on port 8501

Run without the script (manual / learning mode)

1) Start Ollama (as a container)
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3

2) Build & run the chatbot
docker build -t visa-chatbot .
# link the app container to the ollama container
docker run -p 8501:8501 --link ollama visa-chatbot

