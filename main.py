import streamlit as st
from admin import display_admin_page
from getStarted import display_get_started
from payment import display_payment_page
from signin import display_sign_in
from signUp import display_sign_up
from order import display_order_page
from homepage import display_homepage

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "Get Started"

if "user_type" not in st.session_state:
    st.session_state["user_type"] = None  # Initialize user type as None

# Navigation
if st.session_state["page"] == "Get Started":
    display_get_started()
elif st.session_state["page"] == "Sign In":
    display_sign_in()
elif st.session_state["page"] == "Sign Up":
    display_sign_up()
elif st.session_state["page"] == "Homepage":
    display_homepage()
elif st.session_state["page"] == "Order":
    if "username" in st.session_state:
        display_order_page(st.session_state["username"])
    else:
        st.error("Please sign in first!")
        st.session_state["page"] = "Sign In"
elif st.session_state["page"] == "Admin":
    if st.session_state["user_type"] == "admin":
        display_admin_page()


elif st.session_state.page == "payment" and 'order' in st.session_state and st.session_state.order is not None:
    # Extract required fields from the stored order in session state
    order = st.session_state.order

    # Ensure all required keys are present in the order dictionary
    username = order.get('Username', 'Guest')
    order_details = order
    total_price = float(order.get('Price (RM)', 0.00))
    branch = order.get('Branch')
    payment_method = order.get('Payment Method')
    booking_number = order.get('Booking Number', 'N/A')
    prep_time = order.get('Preparation Time (min)', 'N/A')
    


    # Call the display_payment_page function with validated data
    display_payment_page(
        username=username,
        order_details=order_details,
        total_price=total_price,
        branch=branch,
        payment_method=payment_method,
        booking_number=booking_number,
        prep_time=prep_time,

    )

