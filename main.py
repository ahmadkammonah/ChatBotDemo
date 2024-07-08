# Import Libraries
import streamlit as st
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()


# TODO: Add history functionality
def get_gemini_response(question):
    text_response = []
    responses = chat.send_message(question, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    streamed_output = "".join(text_response)

    for word in streamed_output.split():
        yield word + " "
        time.sleep(0.005)


# TODO: Add functionality to submit images.
def on_submit():
    user_input = st.session_state.user_input
    output = get_gemini_response(user_input, st.session_state['past'])
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

    st.session_state.user_input = ''


def on_clear():
    del st.session_state.messages[:]


if __name__ == '__main__':

    user_container = st.container()
    with user_container:
        st.title("💬 Chatbot")
        st.write(
            "This is a simple chatbot that uses Google's Gemini-1.5-flash to generate responses. "
        )
        st.button("Clear message", on_click=on_clear)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        print(st.session_state.messages)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = get_gemini_response(prompt)

        # Stream the response to the chat using `st.write_stream`, then store it in
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
