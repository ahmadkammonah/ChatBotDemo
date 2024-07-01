# Import Libraries
import streamlit as st
from streamlit_chat import message
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
## function to load Gemini Pro model and get response
model= genai.GenerativeModel("gemini-1.5-flash")

#TODO: Add history funcionality
def get_gemini_response(question, history):
    chat = model.start_chat(history=[])
    response=chat.send_message(question)
    for chunk in response:
        output = chunk.text
    return output

#TODO: Add functionality to submit images.
def on_Submit():
    user_input = st.session_state.user_input
    output = get_gemini_response(user_input, st.session_state['past'])
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

    st.session_state.user_input = ''

def on_Clear():
    del st.session_state.past[:]
    del st.session_state.generated[:]


if __name__ == '__main__':
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything 🤗"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]

    st.title("ChatBot")
    response_container = st.empty()


    # container for the chat history
    response_container = st.container()
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

    # container for the user's text input
    user_container = st.container()
    with user_container:
        st.button("Clear message", on_click=on_Clear)
        st.text_input('User Input:', key='user_input', on_change=on_Submit)




