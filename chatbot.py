import openai
import streamlit as st

st.title("Ask Me Bot")

# Ensure the API key is available
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found in secrets.toml")
    st.stop()

# Initialize session state variables if they don't exist
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new user message
prompt = st.chat_input("What is up?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        
        full_response = response.choices[0].message["content"]
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
