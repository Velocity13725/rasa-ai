import streamlit as st
import requests

st.title("Rasa Chatbot with Real-time World Knowledge")

# Function to send the user's input to Rasa and get the response
def get_rasa_response(message):
    payload = {
        "sender": "user",
        "message": message
    }
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
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
    rasa_response = get_rasa_response(user_message)
    bot_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn't understand that."
    st.session_state.history.append(f"Bot: {bot_message}")

# Display the conversation
for message in st.session_state.history:
    st.write(message)
