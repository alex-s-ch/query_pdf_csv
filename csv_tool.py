import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib
from htmlTemplates import css, bot_template, user_template


matplotlib.use('TkAgg')

load_dotenv()

API_key = os.environ['OPENAI_API_KEY']

llm = OpenAI(api_token=API_key)
pandas_ai = PandasAI(llm)


class ChatMessage:
    def __init__(self, message_type, content):
        self.type = message_type
        self.content = content


def csv_tool():
    st.write(css, unsafe_allow_html=True)

    st.header("Query your CSV :bar_chart:")

    with st.sidebar:
        st.subheader("Your CSV file")
        uploaded_file = st.file_uploader('Upload a CSV file here', type=['csv'], key='csv_upload')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head(3))

        if "csv_chat_history" not in st.session_state:
            st.session_state.csv_chat_history = []

        prompt = st.text_area('Enter your prompt:')

        if st.button('Generate'):
            if prompt:
                with st.spinner('Generating response...'):
                    user_message = ChatMessage("user", prompt)
                    st.session_state.csv_chat_history.append(user_message)

                    response = pandas_ai.run(df, prompt=prompt)

                    response_content = response.content if hasattr(response, 'content') else str(response)

                    bot_message = ChatMessage("bot", response_content)
                    st.session_state.csv_chat_history.append(bot_message)

                    for message in st.session_state.csv_chat_history:
                        if message.type == "user":
                            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                        else:
                            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

            else:
                st.warning('Please enter a prompt.')
