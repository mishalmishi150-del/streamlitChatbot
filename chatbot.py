import os 
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

#Load API KEy from.env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.title("Groq chatbot")
st.caption("Ask anything below")

st.divider()
with st.form("chat_from"):
    user_input= st.text_area("Your Message", placeholder="type your question here...")
    submit= st.form_submit_button("send")

if submit:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=30,
        max_retries=2,
        api_key=api_key


    )
   