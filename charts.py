import pandas as pd
import streamlit as st


def show_emission_bar_chart(activity_data):

    if not activity_data:
        st.warning("No data available for chart.")
        return

    df = pd.DataFrame(activity_data)

    chart_data = df[["transport", "electricity"]]

    st.bar_chart(chart_data)


def show_emission_trend(activity_data):

    if not activity_data:
        return

    df = pd.DataFrame(activity_data)

    st.line_chart(df["emission"])