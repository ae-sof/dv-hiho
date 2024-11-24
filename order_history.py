import os
import pandas as pd
import streamlit as st
from display_sidebar import add_notification

orders_file = 'orders.csv'

# Function to display order history and allow updates
def display_order_history(username):  # Accept the username as a parameter
    st.title("Order History")

    if os.path.isfile(orders_file):
        orders_df = pd.read_csv(orders_file)
    else:
        st.info("No orders found.")
        return

    # Initialize session state for notifications if not already done
    if 'notified_orders' not in st.session_state:
        st.session_state.notified_orders = set()

    # Filter options
    st.subheader("Filter Orders")
    filter_status = st.selectbox("Filter by Status", ['All', 'Preparing', 'Ready for Pickup', 'Done'])
    filter_branch = st.selectbox("Filter by Branch", ['All'] + list(orders_df['Branch'].unique()))
    filter_username = st.text_input("Filter by Username", "")

    # Apply filters
    if filter_status != 'All':
        orders_df = orders_df[orders_df['Status'] == filter_status]
    if filter_branch != 'All':
        orders_df = orders_df[orders_df['Branch'] == filter_branch]
    if filter_username:
        orders_df = orders_df[orders_df['Username'].str.contains(filter_username, case=False, na=False)]

    if orders_df.empty:
        st.info("No orders found based on the selected filters.")
        return

    st.write("### Order History")
    st.dataframe(orders_df)

    # Update order status
    for index, order in orders_df.iterrows():
        order_id = order['Booking Number']
        current_status = order['Status'] if pd.notna(order['Status']) else 'Preparing'

        st.subheader(f"Order #{order_id}")
        st.write(f"**Coffee Type**: {order['Coffee Type']}")
        st.write(f"**Username**: {order['Username']}")
        st.write(f"**Branch**: {order['Branch']}")
        st.write(f"**Order Time**: {order['Order Time']}")
        st.write(f"**Current Status**: {current_status}")

        # Use a unique key for each widget by appending the order ID or index
        selectbox_key = f"status_{order_id}_{index}"
        button_key = f"update_{order_id}_{index}"

        # Dropdown to change status
        new_status = st.selectbox(
            f"Update status for Order #{order_id}",
            ['Preparing', 'Ready for Pickup', 'Done'],
            index=['Preparing', 'Ready for Pickup', 'Done'].index(current_status),
            key=selectbox_key
        )

        # Button to update the order status
        if st.button(f"Update Status for Order #{order_id}", key=button_key):

            # Update the status in the DataFrame
            orders_df.loc[orders_df['Booking Number'] == order_id, 'Current Status'] = new_status
            orders_df.to_csv(orders_file, index=False)

            # If the status is updated to anything other than "Preparing", add notification
            if new_status != 'Preparing':
                if order_id not in st.session_state.notified_orders:
                    notification_msg = f"Order #{order_id} status updated to **{new_status}**."
                    add_notification(order['Username'], notification_msg)  # Add notification for the user
                    st.session_state.notified_orders.add(order_id)  # Mark this order as notified
                    st.success(f"Order #{order_id} status updated to **{new_status}**.")
                
