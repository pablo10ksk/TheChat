# https://docs.streamlit.io/
# streamlit run main.py - python -m streamlit run main.py
# from datetime import time

import streamlit as st
from executerequest import eazybase
import uuid
import os
import countryflag
import country_operations
from dotenv import load_dotenv

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # st.session_state["phone"] = str(uuid.uuid4())
    st.session_state["company_owner"] = 0
    st.session_state["phone"] = str(f"{uuid.uuid4()}")
    st.session_state["eazybase"] = eazybase(st.session_state["phone"])
    st.set_page_config(layout="wide")


def repr_agg_data(array_data: dict) -> None:
    if os.getenv("SHOW_SOURCES") == 1:
        for agg_data in array_data:
            with st.expander(agg_data["kbase"], expanded=False):
                st.markdown(agg_data["description"])

    for agg_data in array_data:
        with st.expander(agg_data["kbase"], expanded=False):
            base_ = agg_data["description"]
            if "<pre class=" in base_:
                base_ = base_.replace(
                    '<pre class="language-javascript"><code>', "```javascript \n"
                ).replace("</code></pre>", "\n ```")
            st.markdown(base_)


def submit_auth(country_selected: str, phone_num: str, code: str) -> bool:
    phone_num = f"{country_operations.get_country_code(country_selected)}{phone_num}"
    st.session_state["phone"] = phone_num
    st.session_state["eazybase"].do_login(phone_num, code)


def set_company_combo():
    selected_ = st.selectbox(
        "Company Owner", st.session_state["eazybase"].get_company_lst(), index=0
    )
    st.session_state["eazybase"].set_company_owner(selected_)


def set_count_option():
    country_dict = country_operations.get_countries_map()
    # Create a dropdown list
    return st.selectbox(
        "Select a country",
        options=list(country_dict.keys()),
        format_func=lambda x: f"{x} - {country_dict[x]}",
    )


def set_user_phone():
    st.write(f"Current number: {st.session_state['phone']}")
    if st.session_state["eazybase"].isLogged():
        st.write(f"Login correct!")
    else:
        code_auth = ""
        col1, col2 = st.columns(2)
        with col1:
            country_selected = set_count_option()
        with col2:
            phone_num = st.text_input("Phone number")

        if st.session_state["eazybase"].isrequested():
            code_auth = st.text_input("Code")

        submitted1 = st.button(
            label="Submit",
            on_click=submit_auth,
            args=(
                country_selected,
                phone_num,
                code_auth,
            ),
        )


def _set_chat_space():
    if prompt := st.chat_input("............TheChat.........."):
        st.session_state.messages.append({"name": "user", "text": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Ya mismo te contesto..."):
                response_text, response_data = st.session_state["eazybase"].GetResponse(
                    prompt,
                )
                st.session_state.messages.append(
                    {
                        "name": "assistant",
                        "text": response_text,
                        "extra_data": response_data,
                    }
                )
                # st.write_stream(response_text)
                st.write(response_text)
                repr_agg_data(response_data)


def _set_gdata_space():
    if st.session_state["eazybase"].gather_data():
        st.session_state["eazybase"]._get_usr_gatherdata()
    for objproc in st.session_state["eazybase"].current_gdata:
        st.write(st.session_state["eazybase"].get_text_description(objproc))


def _set_sidebar():
    with st.sidebar:
        set_company_combo()
        set_user_phone()


def _set_ui():
    _set_sidebar()

    if st.session_state["eazybase"].isLogged():
        _set_chat_history()
        _set_chat_space()
    else:
        _set_chat_history()
        _set_chat_space()


def _set_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["name"]):
            st.markdown(message["text"])
            if message["name"] == "assistant" and "extra_data" in message:
                repr_agg_data(message["extra_data"])


_set_ui()
