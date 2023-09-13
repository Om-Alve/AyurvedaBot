import streamlit as st
from streamlit_chat import message as st_message

 
questions = [
        "how are you?",
        "what is your name?"
        ]
if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append({"message":"Hello there!","is_user":False})
count=0

def generate_answer():
    global count
    if count >= len(questions):
        st.session_state.history.append({"message":"Thank you for answering all the questions",
                                         "is_user":False})
    else:
        st.session_state.history.append({"message":questions[count],"is_user":False})
        st.session_state.history.append({"message":st.session_state.input_text,"is_user":True})
        count+=1


user_input = st.text_input("Talk to the bot",key="input_text",on_change=generate_answer)

for i,chat in enumerate(st.session_state.history):
    st_message(**chat,key=str(i))

print(st.session_state.history)
