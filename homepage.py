import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime
from history import display_order_history
from order import display_order_page
from payment import display_payment_page
from display_sidebar import display_cust_sidebar


def logout():
    st.session_state.clear()  # Clears all session state variables (e.g., user_type, username)
    st.session_state["page"] = "Sign In"  # Redirect the user to the Sign In page
    st.rerun()
# Function to load loyalty data
def load_loyalty_data():
    if os.path.isfile('loyalty_points.csv'):
        return pd.read_csv('loyalty_points.csv')
    return pd.DataFrame(columns=['Username', 'Total Price', 'Redeem', 'Loyalty', 'Last Voucher'])


# Function to update loyalty data based on orders
def update_loyalty_points():
    loyalty_df = load_loyalty_data()

    # Load orders and calculate total spent by the user
    if os.path.isfile('orders.csv'):
        orders_df = pd.read_csv('orders.csv')
        total_spent = orders_df[orders_df['Username'] == st.session_state['username']]['Price'].sum()
    else:
        total_spent = 0

    # Check if the user exists in the loyalty data
    user_record = loyalty_df[loyalty_df['Username'] == st.session_state['username']]
    if not user_record.empty:
        # Update existing user's total price and loyalty points
        redeemed_points = user_record['Redeem'].iloc[0]
        loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Total Price'] = total_spent
        loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Loyalty'] = total_spent - redeemed_points
    else:
        # Create a new record for the user
        new_record = {
            'Username': st.session_state['username'],
            'Total Price': total_spent,
            'Redeem': 0,
            'Loyalty': total_spent,
            'Last Voucher': None
        }
        loyalty_df = pd.concat([loyalty_df, pd.DataFrame([new_record])], ignore_index=True)

    # Update session state
    st.session_state["loyalty_points"] = loyalty_df[loyalty_df['Username'] == st.session_state['username']]['Loyalty'].iloc[0]

    # Save the updated loyalty data
    loyalty_df.to_csv('loyalty_points.csv', index=False)


# Function to save the redeemed voucher as an active coupon
def save_coupon(voucher_code, discount, username):
    # Check if the coupons file exists
    if os.path.isfile('coupons.csv'):
        coupons_df = pd.read_csv('coupons.csv')
    else:
        coupons_df = pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active", "Username"])

    # Generate a random expiration date (e.g., 7 days from now)
    expiration_date = (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d")

    # Add the new coupon to the DataFrame
    new_coupon = {
        "Coupon Code": voucher_code,
        "Discount (%)": discount,
        "Expiration Date": expiration_date,
        "Active": True,
        "Username": username
    }
    coupons_df = pd.concat([coupons_df, pd.DataFrame([new_coupon])], ignore_index=True)

    # Save the updated coupons data
    coupons_df.to_csv('coupons.csv', index=False)


# Updated redeem_voucher function
def redeem_voucher():
    if "loyalty_points" not in st.session_state:
        st.session_state["loyalty_points"] = 0

    # Voucher options based on loyalty points
    voucher_options = {
        "5% Off (10 Points)": {"discount": 5, "required_points": 10},
        "10% Off (100 Points)": {"discount": 10, "required_points": 100},
        "15% Off (150 Points)": {"discount": 15, "required_points": 150}
    }

    # Check for available vouchers
    available_vouchers = {
        k: v for k, v in voucher_options.items() if st.session_state["loyalty_points"] >= v["required_points"]
    }

    if available_vouchers:
        selected_voucher = st.selectbox("Select a voucher to redeem", options=list(available_vouchers.keys()))

        if st.button("Redeem Voucher"):
            voucher_details = available_vouchers[selected_voucher]
            required_points = voucher_details["required_points"]
            discount = voucher_details["discount"]

            # Deduct points and update data
            st.session_state["loyalty_points"] -= required_points
            loyalty_df = load_loyalty_data()

            # Generate a unique voucher code
            voucher_code = f"{selected_voucher.split()[0].upper()}-{random.randint(1000, 9999)}"

            # Update user's loyalty record
            user_record = loyalty_df[loyalty_df['Username'] == st.session_state['username']]
            if not user_record.empty:
                current_redeem = user_record['Redeem'].iloc[0]
                new_redeem = current_redeem + required_points

                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Redeem'] = new_redeem
                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Loyalty'] = \
                    loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Total Price'] - new_redeem
                loyalty_df.loc[loyalty_df['Username'] == st.session_state['username'], 'Last Voucher'] = selected_voucher
            else:
                # Create a new record if user not found
                new_record = {
                    'Username': st.session_state['username'],
                    'Total Price': 0,
                    'Redeem': required_points,
                    'Loyalty': st.session_state["loyalty_points"],
                    'Last Voucher': selected_voucher
                }
                loyalty_df = pd.concat([loyalty_df, pd.DataFrame([new_record])], ignore_index=True)

            # Save the updated loyalty data
            loyalty_df.to_csv('loyalty_points.csv', index=False)

            # Save the voucher as an active coupon
            save_coupon(voucher_code, discount, st.session_state['username'])

            # Success message for voucher redemption
            st.success(f"You have successfully redeemed a {discount}% off voucher!")
            st.write(f"🎟️ Your voucher code is: `{voucher_code}`")
            st.markdown(f"🎉 **Your new loyalty balance:** {st.session_state['loyalty_points']} points")
            st.rerun()
    else:
        st.info("You don't have enough points to redeem any vouchers at the moment.")

# Display active coupons
def load_active_coupons(username):
    if os.path.isfile('coupons.csv'):
        coupons_df = pd.read_csv('coupons.csv')
    else:
        # Create an empty DataFrame if file doesn't exist
        coupons_df = pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active", "Username"])
    
    # Filter active coupons for the given user or those available to all
    active_coupons = coupons_df[
        (coupons_df['Active'] == 'True') &  # Only active coupons
        ((coupons_df['Username'] == username) | (coupons_df['Username'] == "all"))
    ]

    
    return active_coupons

def load_past_coupons(username):
    if os.path.isfile('coupons.csv'):
        coupons_df = pd.read_csv('coupons.csv')
    else:
        # Create an empty DataFrame if file doesn't exist
        coupons_df = pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active", "Username"])
    
    # Filter active coupons for the given user or those available to all
    past_coupons = coupons_df[
        (coupons_df['Active'] == 'False') &  # Only active coupons
        ((coupons_df['Username'] == username) | (coupons_df['Username'] == "all"))
    ]

    
    return past_coupons


def display_homepage():
    coupons_df = pd.read_csv('coupons.csv')
    if 'username' not in st.session_state:
        st.error("Please sign in to access this page.")
        return

    username = st.session_state['username']
    page = display_cust_sidebar(username)

    if page == "Homepage":
        # Welcome User
        st.subheader(f"Welcome back, {username}!")

        # Update and display loyalty points
        update_loyalty_points()
        st.markdown(f"""
        <div style="background-color: #f9f7f6; padding: 20px; margin-top: 20px; border-radius: 10px; text-align: center; border: 2px solid #4CAF50;">
            <h2 style="color: #27ae60; margin: 0;">🎉 {int(st.session_state['loyalty_points'])} Loyalty Points</h2>
            <p style="font-size: 16px; color: #2d3436;">Earn more points with every purchase to unlock amazing rewards!</p>
        </div>
        """, unsafe_allow_html=True)

        # Redeem a voucher section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🎁 Redeem a Voucher")
        st.write("Redeem your points for exciting discounts on your next purchase.")
        redeem_voucher()

        # Active Coupons Section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🌟 Active Coupons")
        active_coupons = load_active_coupons(username)
        if not active_coupons.empty:
            for _, coupon in active_coupons.iterrows():
                st.markdown(f"""
                <div style="background-color: #e0f7fa; padding: 20px; margin-bottom: 15px; border-radius: 10px; border-left: 5px solid #009688;">
                    <h4 style="color: #00796b; font-size: 22px;">🎟️ <strong>{coupon['Coupon Code']}</strong></h4>
                    <p style="font-size: 18px; color: #00796b;">**Discount**: {coupon['Discount (%)']}% Off</p>
                    <p style="font-size: 16px; color: #444;">**Expires On**: {coupon['Expiration Date']}</p>
                    <div style="font-size: 18px; color: #388e3c;">
                        <strong>Active</strong> ✔️
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active coupons available at the moment.")
        # Past Coupons Section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📜 Past Coupons")
        past_coupons = load_past_coupons(username)

        if not past_coupons.empty:
            for _, coupon in past_coupons.iterrows():
                st.markdown(f"""
                <div style="background-color: #fbe9e7; padding: 20px; margin-bottom: 15px; border-radius: 10px; border-left: 5px solid #d84315;">
                    <h4 style="color: #e64a19; font-size: 22px;">🎟️ <strong>{coupon['Coupon Code']}</strong></h4>
                    <p style="font-size: 18px; color: #d84315;">**Discount**: {coupon['Discount (%)']}% Off</p>
                    <p style="font-size: 16px; color: #444;">**Expired On**: {coupon['Expiration Date']}</p>
                    <div style="font-size: 18px; color: #c62828;">
                        <strong>Inactive</strong> ❌
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No past coupons available at the moment.")

    elif page == "Order":
        display_order_page(username)

    elif page == "History":
        display_order_history()

    if st.sidebar.button('Logout'):
        logout()  # Call the logout function when the button is clicked
