import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="AI Partner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.title("AI智能伴侣")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])


@st.cache_resource
def get_client():
    return OpenAI(api_key=os.getenv('DOUBAO_API_KEY'), base_url="https://ark.cn-beijing.volces.com/api/v3")

client = get_client()

prompt = st.chat_input("请输入您的问题或需求...")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="doubao-seed-2-0-mini-260215",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.messages,
        ],
        stream=True,
        temperature=1.3
    )

    response_message = st.empty()
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_content += content
            response_message.chat_message("assistant").write(full_content)

    st.session_state.messages.append({"role": "assistant", "content": full_content})
