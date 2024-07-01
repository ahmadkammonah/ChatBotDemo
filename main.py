# Import Libraries
import streamlit as st
from streamlit_chat import message


def on_Submit():
    user_input = st.session_state.user_input
    output = user_input
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




