import os
from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import streamlit as st

load_dotenv(override=True)
api_key=os.getenv('OPENAI_API_KEY')
client=OpenAI()
app=st.title("AI Business Assistant")
if "chatHistory" not in st.session_state:
    st.session_state.chatHistory=[
        {
            "role":"system",
            "content": (
                "You will answer the question as per requirement. Once you answered, "
                "you will prompt the user if he/she would like to continue. If No, "
                "you need to say goodbye in polite manner. This is a business environment "
                "and you are expected to maintain decorum."
            )
        }
    ]
for message in st.session_state.chatHistory:
    if message["role"]!="system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

msg=st.chat_input("Hello, How can I help you?")
if msg:
    with st.chat_message("user"):
        st.write(msg)
    st.session_state.chatHistory.append({"role":"user", "content":msg})
    try:
        res=client.chat.completions.create(model="gpt-4.1-nano", messages=st.session_state.chatHistory)
        response=res.choices[0].message.content
        with st.chat_message("assistant"):
            st.write(response)
            st.session_state.chatHistory.append({"role":"assistant","content":response})
    except Exception as e:
        st.error(f"Error occured: {e}")
        
        

