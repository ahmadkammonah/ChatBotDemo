from streamlit_chat import message
import streamlit as st


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append({"type": "text", "data": user_input})
    st.session_state.generated.append({"type": "text", "data": user_input})  # Echo back the user input


def on_image_upload():
    uploaded_file = st.session_state.image_uploader
    if uploaded_file is not None:
        pass
        # st.session_state.past.append({"type": "image", "data": uploaded_file})
        # st.session_state.generated.append({"type": "image", "data": uploaded_file})  # Echo back the uploaded image


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


if __name__ == '__main__':
    # Initialize session state if not already done
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    st.title("ChatBot test")

    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            if st.session_state['past'][i]['type'] == "text":
                message(st.session_state['past'][i]['data'], is_user=True, key=f"{i}_user", avatar_style='no-avatar')
            elif st.session_state['past'][i]['type'] == "image":
                st.image(st.session_state['past'][i]['data'], caption="User", use_column_width=True,
                         key=f"{i}_user_image")

            if st.session_state['generated'][i]['type'] == "text":
                message(st.session_state['generated'][i]['data'], key=f"{i}", allow_html=True, avatar_style='no-avatar')
            elif st.session_state['generated'][i]['type'] == "image":
                st.image(st.session_state['generated'][i]['data'], caption="Bot", use_column_width=True,
                         key=f"{i}_bot_image")

        st.button("Clear message", on_click=on_btn_click)

    with st.container():
        st.text_input("User Input:", on_change=on_input_change, key="user_input")
        st.file_uploader("Upload an Image:", on_change=on_image_upload, key="image_uploader")
