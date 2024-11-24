import streamlit as st
from inventory import display_inventory_management
from sales_page import display_sales_reporting
from analytics import display_analytics_dashboard
from order_history import display_order_history
from coupon import display_promotions_page  # Import the promotions functionality
from display_sidebar import display_admin_notifications  # Function to display admin notifications

# Function to clear session state and log the user out
def logout():
    st.session_state.clear()  # Clears all session state variables (e.g., user_type, username)
    st.session_state["page"] = "Sign In"  # Redirect the user to the Sign In page
    st.rerun()  # Refresh the app to show the Sign In page


# Function to display the admin page with navigation and notifications
def display_admin_page():
    # Sidebar title and logout button
    st.sidebar.title("Admin Dashboard")
    
    
    # Page navigation in the sidebar
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Order History", "Inventory Management", "Sales Reporting", "Analytics Dashboard", "Promotions & Discounts"]
    )
    # Display admin notifications after navigation
    username = st.session_state.get('username', 'default_user') 
    # Handle different page navigation based on the selection
    if page == "Order History":
        display_order_history(username)  # Pass the username to display_order_history
    elif page == "Inventory Management":
        display_inventory_management()
    elif page == "Sales Reporting":
        display_sales_reporting()  # Correct function call
    elif page == "Analytics Dashboard":
        display_analytics_dashboard()
    elif page == "Promotions & Discounts":
        display_promotions_page()  # Display promotions and coupon management page
    
     # Fetch username from session
    display_admin_notifications(username)  # Display notifications for the admin
    # Add Logout button to the sidebar
    if st.sidebar.button('Logout'):
        logout()  # Call the logout function when the button is clicked


# Show the login page if the user is not logged in
def display_login_page():
    st.title("Please Sign In")
    st.write("You need to sign in to access the admin page.")

if __name__ == "__main__":
    # Ensure that the session state is properly initialized
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = None  # No user logged in initially
    if "page" not in st.session_state:
        st.session_state["page"] = "Sign In"  # Set default page to Sign In

    # Add the username to the session state (simulate login process)
    if "username" not in st.session_state:
        st.session_state["username"] = 'admin'  # Default username, change after real login

    # Display the admin page if the user is an admin
    if st.session_state.user_type == 'admin':  
        display_admin_page()  # Admin dashboard page with logout option
    else:
        # Show login page if the user is not logged in or is not an admin
        display_login_page()
