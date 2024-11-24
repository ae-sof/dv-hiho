import streamlit as st

def display_get_started():
    st.title("☕DeeVee Hiho Cafe☕")
    st.image("logo.png")
    if st.button("Get Started"):
        st.session_state["page"] = "Sign In"

