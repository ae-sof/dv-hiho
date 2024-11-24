import bcrypt
import pandas as pd
import streamlit as st

USER_DB = "users.csv"  # Path to the user database

# Load user data
def load_user_data():
    if not pd.io.common.file_exists(USER_DB):
        return pd.DataFrame(columns=["user_id", "username", "password"])
    return pd.read_csv(USER_DB)

# Verify the password
def verify_password(entered_password, stored_password):
    return bcrypt.checkpw(entered_password.encode(), stored_password.encode())

# Sign-In Logic
def user_sign_in(username, password):
    users_df = load_user_data()

    # Check for admin account (default credentials)
    if username == "admin" and password == "admin":
        st.session_state["user_type"] = "admin" 
        return "Admin"  # Special role for admin access

    # Check if the username exists in the user database
    user_record = users_df[users_df["username"] == username]
    if not user_record.empty:
        stored_password = user_record.iloc[0]["password"]
        if verify_password(password, stored_password):
            return "User"  # Regular user access
        else:
            st.error("Invalid password.")
            return None
    else:
        st.error("Username not found.")
        return None

# Display Sign-In Page
def display_sign_in():
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if username and password:
            role = user_sign_in(username, password)  # Get the role (Admin/User)
            if role:
                st.session_state["username"] = username
                if role == "Admin":
                    st.session_state["page"] = "Admin"
                    st.success("Redirecting to Admin Page...")
                else:
                    st.session_state["page"] = "Homepage"
                    st.success("Redirecting to Home Page...")

    # Place "Don't have an account?" and Sign-Up button side by side
    col1, col2 = st.columns([0.4, 1])  # Adjust column width ratios as needed
    with col1:
        st.write("Don't have an account?")
    with col2:
        if st.button("Go to Sign Up"):
            st.session_state["page"] = "Sign Up"
