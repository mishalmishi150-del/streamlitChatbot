import streamlit as st


st.title( "Zeta AI Chatbot")
st.header("This is st.header")
st.subheader("This is st.header")
st.caption("This is st.caption ? small grey text")
st.divider()

st.subheader("Text")
st.text("Enter uoru Query yo use this CHabto")

st.write("st.write ? work with text, number, dicts, dataframes and more")

st.divider()

#Name input 
st.text_input("Name", placeholder="Enter your name here")
#Email input
st.text_input("Email",placeholder="Enter your email here")

#Message input
st.number_input("Age",min_value=1,max_value=120,value=25)
#country
st.selectbox("Country",["Pakistan","us","Dubai"])
st.multiselect("select your interests",["AI","Machine Learning","Deep Learning",])


