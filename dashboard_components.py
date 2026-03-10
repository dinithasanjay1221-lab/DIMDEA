import streamlit as st


def show_metric(title, value):

    st.metric(
        label=title,
        value=value
    )


def show_section(title):

    st.markdown("---")
    st.subheader(title)