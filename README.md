This is a simple AI chatbot that helps users with UK visa questions.
It uses Streamlit for the web app and Ollama (Llama 3) for local AI responses.

⸻

 What It Does
	•	Lets users chat and ask visa-related questions
	•	Runs fully on your computer (no API keys needed)
	•	Works through Docker or directly with Python

 How to Run (Easiest Way — Docker)

Step 1: Make sure you have Docker Desktop installed and running

If you don’t have it, download it from:
👉 https://www.docker.com/products/docker-desktop

Step 2: Clone this project

Open your terminal and run:
git clone https://github.com/Syedh100/Visa_chatbot.git
cd Visa_chatbot

Step 3: Start everything

Run this command:bash start_chatbot.sh
This will:
	1.	Start Ollama (the AI)
	2.	Download the Llama 3 model (if not already installed)
	3.	Build and run the chatbot automatically

Step 4: Open the chatbot

Once it’s done, go to your browser and visit the link they provide in terminal 
