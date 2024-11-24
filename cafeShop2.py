import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os


#Load user data from CSV

# Define sample menu
menu = {
    'Americano': 2.5,
    'Cappuccino': 3.0,
    'Latte': 3.5,
    'Caramel Macchiato': 4.0
}

# Initialize session state
if 'user_type' not in st.session_state: # 'user_type' referring to admin or customer. 
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Create a placeholder for dynamic content
placeholder = st.empty()

# Function to save orders to CSV
def save_order_to_csv(order):
    # Check if the orders CSV file exists
    if not os.path.isfile('orders.csv'):
        # Create a new CSV file and add headers
        df = pd.DataFrame([order])
        df.to_csv('orders.csv', index=False)
    else:
        # Append to existing CSV file
        df = pd.DataFrame([order])
        df.to_csv('orders.csv', mode='a', header=False, index=False)

# Landing Page
with placeholder.container():
    if st.session_state.user_type is None:
        st.title("Welcome to the Coffee Shop App")
        st.subheader("Please choose your role:")

        # Use buttons to select role
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Customer (Front-End)"):
                st.session_state.user_type = 'customer_signin'
                placeholder.empty()  # Clear the landing page

        with col2:
            if st.button("Admin (Back-End)"):
                st.session_state.user_type = 'admin'
                placeholder.empty()  # Clear the landing page

# Sign In Page for Customers
if st.session_state.user_type == 'customer_signin':
    with placeholder.container():
        st.header("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if username and password:  # Simple check for demonstration
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.session_state.user_type = 'customer_page'  # Redirect to customer page
                placeholder.empty()  # Clear the sign-in page
            else:
                st.error("Please enter both username and password.")

# Customer Page Function
if st.session_state.user_type == 'customer_page':
    with placeholder.container():
        st.title("Customer Portal")
        st.header("Welcome, " + st.session_state.username + "!")

        # Menu Display
        st.header("Menu")
        st.write(pd.DataFrame(list(menu.items()), columns=['Coffee Type', 'Price ($)']))

        # Order placement form
        with st.form(key='order_form'):
            coffee_type = st.selectbox("Select Coffee", list(menu.keys()))
            size = st.radio("Select Size", ['Small', 'Medium', 'Large'])
            add_ons = st.multiselect("Add-ons", ['Extra Sugar', 'Milk', 'Whipped Cream','Less Sugar'])
            submit_order = st.form_submit_button("Place Order")

            if submit_order:
                booking_number = str(random.randint(1000, 9999))
                prep_time = random.randint(5, 15)
                order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Store order in a dictionary
                order = {
                    'Username': st.session_state.username,
                    'Coffee Type': coffee_type,
                    'Size': size,
                    'Add-ons': add_ons,
                    'Booking Number': booking_number,
                    'Preparation Time (min)': prep_time,
                    'Order Time': order_time
                }
                
                # Save order to CSV
                save_order_to_csv(order)

                # Display confirmation
                st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")


        # Feedback
        st.header("Feedback")
        feedback = st.text_area("Leave your feedback here:")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

        # Button to go back to the landing page
        if st.button("Go back to landing page"):
            st.session_state.user_type = None
            st.session_state.username = None  # Reset username on going back
            placeholder.empty()  # Clear the customer page

# Admin Pages
if st.session_state.user_type == 'admin':
    with placeholder.container():
        st.sidebar.title("Admin Pages")
        admin_page = st.sidebar.selectbox("Go to", ["Order History", "Inventory Management", "Sales Reporting", "Analytics Dashboard", "Notifications"])
        st.write("Explore the Menu option for Inventory Management, Sales Reporting, Analytics Dashboard, and Notifications")

        # Order History Page
        if admin_page == "Order History":
            st.title("Order History")

            # Load order history from CSV
            if os.path.isfile('orders.csv'):
                order_history = pd.read_csv('orders.csv', dtype={'Booking Number': str})
                
                # Display orders
                st.write(order_history)

                # Select and delete an order
                if not order_history.empty:
                    delete_order = st.selectbox("Select Booking Number to Delete", order_history['Booking Number'].unique())
                    if st.button("Delete Order"):
                        order_history = order_history[order_history['Booking Number'] != delete_order]
                        order_history.to_csv('orders.csv', index=False)
                        st.success(f"Order with Booking Number {delete_order} has been deleted.")
            else:
                st.info("No orders placed yet.")

        # Inventory Management Page
        if admin_page == "Inventory Management":
            st.title("Inventory Management")
            st.write("This page will manage inventory.")  # Placeholder for future functionality

        # Button to go back to the landing page
        if st.button("Go back to landing page"):
            st.session_state.user_type = None
            st.session_state.username = None  # Reset username on going back
            placeholder.empty()  # Clear the admin page
