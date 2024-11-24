import pandas as pd
import streamlit as st
import bcrypt

USER_DB = "users.csv"  # Path to the user database

def hash_password(password):
    # Generate a hashed password.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def load_user_data():
    """Load user data from CSV file."""
    if not pd.io.common.file_exists(USER_DB):
        return pd.DataFrame(columns=["user_id", "username", "password"])
    return pd.read_csv(USER_DB)

def save_user_data(users_df):
    """Save user data to CSV file."""
    users_df.to_csv(USER_DB, index=False)

def user_sign_up(username, password):
    """Handle user sign-up logic."""
    users_df = load_user_data()

    # Check if the username already exists
    if username in users_df["username"].values:
        st.error("Username already exists! Please choose a different username.")
    else:
        # Generate a unique user ID
        user_id = len(users_df) + 1

        # Add new user to the database with hashed password
        hashed_password = hash_password(password)
        new_user = {
            "user_id": user_id,
            "username": username,
            "password": hashed_password,
        }
        users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
        save_user_data(users_df)
        st.success("Sign-up successful! You can now log in.")

def display_sign_up():
    """Display the sign-up form."""
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if username and password and confirm_password:
            if password == confirm_password:
                user_sign_up(username, password)
                st.session_state["page"] = "Sign In"
            else:
                st.error("Passwords do not match.")
        else:
            st.error("Please provide all required information.")

    # Adjust the layout for "Already have an account?" and the Sign-In button
    col1, col2 = st.columns([1.5, 3.5])  # Adjust column widths to bring them closer
    with col1:
        st.write("Already have an account?")
    with col2:
        if st.button("Sign In"):
            st.session_state["page"] = "Sign In"
