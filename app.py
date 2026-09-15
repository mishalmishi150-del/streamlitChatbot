import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env file
load_dotenv()

st.set_page_config(
    page_title="Chatbot",
)

st.title("Chatbot")

# Get Groq API key from .env
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key nahi mili. .env file check karein.")
    st.stop()

# Groq AI
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    groq_api_key=api_key
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_message = st.chat_input("Type your message...")

if user_message:

    # Show user message
    with st.chat_message("user"):
        st.write(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Get AI response
    try:
        response = llm.invoke(user_message)

        # Show AI response
        with st.chat_message("assistant"):
            st.write(response.content)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.content
        })

    except Exception as e:
        st.error("Groq API mein error aa raha hai.")
        st.code(str(e))

