import csv
import os
from datetime import datetime
import streamlit as st

# Path to the CSV file that stores notifications
NOTIFICATION_FILE = "user_notifications.csv"

# Function to read notifications from CSV
def read_notifications():
    notifications = {}
    if os.path.exists(NOTIFICATION_FILE):
        with open(NOTIFICATION_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[0]
                notification_msg = row[1]
                if username not in notifications:
                    notifications[username] = []
                notifications[username].append(notification_msg)
    return notifications

# Function to save a notification to CSV
def save_notification(username, notification_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTIFICATION_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, notification_msg, timestamp])

# Function to clear notifications for a specific user
def clear_notifications(username):
    notifications = read_notifications()
    updated_notifications = {key: [] for key in notifications.keys()}  # Initialize empty list for each user

    # Overwrite the CSV with cleared notifications for the user
    with open(NOTIFICATION_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for user, msgs in notifications.items():
            if user != username:
                for msg in msgs:
                    writer.writerow([user, msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    return "Notifications cleared!"

# Function to display notifications in the sidebar for a user
def display_user_notifications(username):
    st.sidebar.subheader(f"🔔 Notifications for {username}")
    notifications = get_notifications(username)

    if notifications:
        for notification in notifications:
            st.sidebar.info(notification)

        # Clear notifications button
        if st.sidebar.button("Clear Notifications", key=f"clear_{username}"):
            clear_notifications(username)
            st.sidebar.success("Notifications cleared!")
    else:
        st.sidebar.info("No notifications at the moment.")

# Function to retrieve notifications for a user
def get_notifications(username):
    notifications = read_notifications()
    if username == 'admin' and username in notifications:
        return [notifications['admin'][-1]]  # Return the latest notification
    return notifications.get(username, [])

# Function to add a notification for a user
def add_notification(username, notification_msg):
    notifications = get_notifications(username)
    if notification_msg not in notifications:
        save_notification(username, notification_msg)  # Save new notification to CSV


# Function to display the customer sidebar with navigation and notifications
def display_cust_sidebar(username):
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["About Us", "Homepage", "Order", "History"], key=f"nav_{username}")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    display_user_notifications(username)
    
     # Add "About Us" section in the sidebar
    if page == "About Us":
        st.title("Welcome to DeeVee Hiho!")
        st.write(
            """
            At DeeVee Heehoo, we aim to deliver a superior coffee experience. 
            Whether you're looking for a cozy spot to relax, a quick coffee to-go, 
            or a place to connect with others, we're here to make your day better.

            ### Our Mission:
            To serve premium coffee with a smile.

            ### Our Vision:
            Creating connections one cup at a time.
            
            ### Meet Our Team:
            At DeeVee Hiho, our talented team is dedicated to ensuring that 
            every customer enjoys a top-notch coffee experience. Here’s a quick introduction to 
            the hard-working team members behind our café project:
            - Nurul Nur Syazwani binti Azriza (20001471)
            - Syarifah Nabilah binti Syed Abdul Rahman (20001090)
            - Alfina Aisyah Binti Abdullah (21001143)
            - Ainin Sofiya Binti Mohd Edyamin (20001438)
            - Muamar Bin Masri (22003363)
            """
        )
    return page



# Function to display admin notifications and manage them
def display_admin_notifications(username):
    st.sidebar.subheader("🔔 Admin Notifications")
    admin_notifications = get_notifications('admin')

    if admin_notifications:
        st.sidebar.info(admin_notifications[0])  # Show only the latest notification
        if st.sidebar.button("Clear Admin Notifications", key=f"clear_admin"):
            clear_notifications('admin')
            st.sidebar.success("Admin Notifications cleared!")
    else:
        st.sidebar.info("No admin notifications.")



