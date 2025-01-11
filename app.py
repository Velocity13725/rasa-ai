import streamlit as st
import requests
import subprocess
from pyngrok import ngrok

st.title("Rasa Chatbot with Real-time World Knowledge")

# Initialize ngrok and start Rasa
if "rasa_url" not in st.session_state:
    # Start the Rasa server in the background
    subprocess.Popen(["rasa", "run", "--enable-api", "--port", "5005"])
    
    # Start ngrok to expose the Rasa server
    public_url = ngrok.connect(5005)  # Port 5005
    st.session_state.rasa_url = public_url
    st.write(f"Rasa server is running at {public_url}/webhooks/rest/webhook")

# Function to send the user's input to Rasa and get the response
def get_rasa_response(message):
    payload = {
        "sender": "user",
        "message": message
    }
    rasa_url = f"{st.session_state.rasa_url}/webhooks/rest/webhook"
    response = requests.post(rasa_url, json=payload)
    return response.json()

# Display chat history if any
if "history" not in st.session_state:
    st.session_state.history = []

# Get user input
user_message = st.text_input("You:", "")

if user_message:
    st.session_state.history.append(f"You: {user_message}")

    # Get response from Rasa
    try:
        rasa_response = get_rasa_response(user_message)
        bot_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn't understand that."
    except Exception as e:
        bot_message = f"Error connecting to Rasa server: {e}"
    
    st.session_state.history.append(f"Bot: {bot_message}")

# Display the conversation
for message in st.session_state.history:
    st.write(message)
