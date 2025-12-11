###########################################################################################
# 1. 설명 : streamlit을 이용한 챗봇 만들기
#         ※ streamlit.io : 터미널 창에서 실행한 내용을 UI로 구현, 파이선 기반 web UI를 쉽게 구현 가능
# 2. 변경 이력
# version          작성자ID           일자                내용
# 1.0              jhlee1101         2025.12.11         최초 작성
###########################################################################################

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# st.sidebar 정의 : 사이드바에 내용을 추가하는 기능
with st.sidebar:
    open_api_key = os.getenv("OPENAI_API_KEY")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬Chatbot")

# st.session_state : 스트림릿에서 사용자의 세션 상태를 관리하는 기능, 사용자가 웹 브라우저에서 상호 작용하는 동안 그상태를 유지하고 업데이트
# 초기 설정이 없으면 대화 시작
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant", "content": "Hello! How can I help you?"}]

# 대화 기록을 웹 브라우저에 출력하는 부분. st.chat_message : 스트림릿의 채팅 인터페이스에서 메시지를 출력하는 용도
# 각 메시지의 역할 : assistant, user
# .write() 로 화면 출력
for msg in st.session_state.message:
    # st.chat_message(msg["role"], msg["content"])  # Streamlit 1.32 이후 st.chat_message()의 함수 시그니처가 바뀌어서 발생하는 전형적인 문제
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자의 입력을 받아 prompt 변수에 반영, st.chat_input은 스트림릿에서 제공하는 기능으로 사용자가 입력한 텍스트를 받아 옴
# open_api_key 가 정의하지 않으면 오류 발생
if prompt := st.chat_input():
    if not open_api_key:
        st.info("Please add you OpenAI key to continue...")
        st.stop()

    # 사용자가 채팅창에 질문을 입력하면 해당 내용을 st.session_state.messages에 딕셔너리 형태로 추가하고 화면에 사용자 입력 내용을 출력
    client = OpenAI(api_key=open_api_key)
    st.session_state.message.append({"role":"user", "content": prompt})
    st.chat_message("user").write(prompt)

    # GPT의 답변을 받아 와서 다시 st.session_state.messages에 추가하고 답변을 화면에 출력
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.message)
    msg = response.choices[0].message.content
    st.session_state.message.append({"role":"assistant", "content": msg})
    st.chat_message("assistant").write(msg)

