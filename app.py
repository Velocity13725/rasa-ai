import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to generate a response from DialoGPT
def generate_response(user_message, chat_history):
    # Encode the user message and add the conversation history
    input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # Append chat history to input
    bot_input_ids = input_ids
    if chat_history:
        bot_input_ids = torch.cat([chat_history, input_ids], dim=-1)

    # Generate a response from the model
    bot_output = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=2, temperature=0.7)
    bot_message = tokenizer.decode(bot_output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return bot_message, bot_input_ids

# Function to fetch the latest information from Wikipedia
def fetch_latest_info(query):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&titles={query}"
    response = requests.get(url).json()
    pages = response['query']['pages']
    page = next(iter(pages.values()))
    extract = page.get('extract', 'Sorry, I couldn\'t fetch any information.')
    return extract

# Display chat history if any
if "history" not in st.session_state:
    st.session_state.history = []

# Add memory functionality to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

# Get user input
user_message = st.text_input("You:", "")

# Respond when the user sends a message
if user_message:
    # Check if user wants to fetch real-time information (e.g., using 'tell me about' or 'what is' pattern)
    if "tell me about" in user_message or "what is" in user_message:
        query = user_message.split("about")[-1] if "about" in user_message else user_message.split("is")[-1]
        info = fetch_latest_info(query.strip())
        st.write(f"Here is the latest info: {info}")
    else:
        # Generate response from DialoGPT and update the chat history
        bot_message, chat_history = generate_response(user_message, st.session_state.chat_history)
        st.session_state.history.append(f"You: {user_message}")
        st.session_state.history.append(f"Bot: {bot_message}")
        st.session_state.chat_history = chat_history

# Display the conversation history
for message in st.session_state.history:
    st.write(message)

