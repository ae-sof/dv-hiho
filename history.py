import os
import pandas as pd
import streamlit as st
import datetime

def display_order_history():
    st.title("Order History")

    # Load orders.csv
    if os.path.isfile("orders.csv"):
        orders_df = pd.read_csv("orders.csv")
    else:
        st.warning("No order history found.")
        return

    # Load feedback.csv (if it exists)
    feedback_df = pd.read_csv("feedback.csv") if os.path.isfile("feedback.csv") else pd.DataFrame()

    username = st.session_state.get("username", "Guest")
    user_orders = orders_df[orders_df["Username"] == username]

    if user_orders.empty:
        st.warning("No orders found for your account.")
        return

    # Improved Display for Each Order
    for _, order in user_orders.iterrows():
        with st.expander(f"Order #{order['Booking Number']} - {order['Coffee Type']} (RM{order['Price']:.2f})"):
            # Order Details
            st.write(f"**Size**: {order['Size']} | **Ice**: {order['Ice']} | **Sugar**: {order['Sugar']}")
            if order['Add-ons']:
                st.write(f"**Add-ons**: {order['Add-ons']}")
            st.write(f"**Order Time**: {order['Order Time']}")
            st.write(f"**Branch**: {order.get('Branch', 'N/A')}")

            # Order Status
            status = order.get('Status', 'Preparing')  # Use .get() to avoid KeyError
            st.write(f"**Status**: {status}")

            # Feedback Section
            existing_feedback = feedback_df[
                (feedback_df["Username"] == username) &
                (feedback_df["Booking Number"] == order["Booking Number"])
            ]

            if not existing_feedback.empty:
                # Feedback already exists
                st.write("### Feedback Submitted")
                st.write(f"**Rating**: {'⭐' * int(existing_feedback.iloc[0].get('Rating', 0))}")
                st.info(f"**Comments**: {existing_feedback.iloc[0].get('Comments', 'No comments provided')}")
            else:
                # Feedback form for new feedback
                st.write("### Provide Your Feedback")
                stars = st.radio(
                    "Rate this order:", [1, 2, 3, 4, 5],
                    format_func=lambda x: "⭐" * x,
                    key=f"rating_{order['Booking Number']}"
                )
                feedback = st.text_area(
                    "Leave a comment:", 
                    placeholder="Share your experience here...", 
                    key=f"comments_{order['Booking Number']}"
                )
                submit_feedback = st.button(
                    f"Submit Feedback for Order #{order['Booking Number']}", 
                    key=f"submit_{order['Booking Number']}"
                )

                if submit_feedback:
                    feedback_entry = {
                        "Username": username,
                        "Booking Number": order["Booking Number"],
                        "Coffee Type": order["Coffee Type"],
                        "Rating": stars,
                        "Comments": feedback,
                        "Feedback Time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # Append feedback to the feedback_df and save it to the feedback.csv file
                    feedback_df = pd.concat([feedback_df, pd.DataFrame([feedback_entry])], ignore_index=True)
                    feedback_df.to_csv("feedback.csv", index=False)

                    st.success("Thank you for your feedback!")
                    st.rerun()

    # Additional Improvements
    st.write("---")
    st.info("**Your feedback helps us improve our service. Thank you!**")
