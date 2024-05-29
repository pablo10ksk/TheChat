# https://docs.streamlit.io/
# streamlit run main.py - python -m streamlit run main.py
# from datetime import time

import streamlit as st
from elasticsearch import Elasticsearch
import json
import webbrowser
from executerequest import eazybase
import uuid


def repr_agg_data(array_data: dict) -> None:
    for agg_data in array_data:
        with st.expander(agg_data["kbase"], expanded=False):
            st.markdown(agg_data["description"])


def submit_auth(phone_num: str, code: str) -> bool:
    st.session_state["eazybase"].do_login(phone_num, code)


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state["phone"] = str(uuid.uuid4())
    st.session_state["company_owner"] = 3
    st.session_state["eazybase"] = eazybase(
        st.session_state["phone"], st.session_state["company_owner"]
    )

if st.session_state["eazybase"].isLogged():
    with st.sidebar:
        if st.session_state["eazybase"].gather_data():
            st.session_state["eazybase"]._get_usr_gatherdata()
        for objproc in st.session_state["eazybase"].current_gdata:
            st.write(st.session_state["eazybase"].get_text_description(objproc))
else:
    with st.sidebar:
        code_auth = ""
        phone_num = st.text_input("Phone number")
        print(phone_num)

        if st.session_state["eazybase"].isrequested():
            code_auth = st.text_input("Code")
        submitted1 = st.button(
            label="Submit",
            on_click=submit_auth,
            args=(
                phone_num,
                code_auth,
            ),
        )
        print(submitted1)


for message in st.session_state.messages:
    with st.chat_message(message["name"]):
        st.write(message["text"])
        if message["name"] == "assistant" and "extra_data" in message:
            repr_agg_data(message["extra_data"])


if prompt := st.chat_input("............TheChat..........just ASK..........."):
    st.session_state.messages.append({"name": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Ya mismo te contesto..."):
            response_text, response_data = st.session_state["eazybase"].GetResponse(
                prompt
            )
            st.session_state.messages.append(
                {
                    "name": "assistant",
                    "text": response_text,
                    "extra_data": response_data,
                }
            )
            st.write(response_text)
            repr_agg_data(response_data)
