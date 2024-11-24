import streamlit as st
import pandas as pd
from datetime import date

coupon_file = 'coupons.csv'

# Function to load existing coupons
def load_coupons():
    if not pd.io.common.file_exists(coupon_file):
        return pd.DataFrame(columns=["Coupon Code", "Discount (%)", "Expiration Date", "Active"])
    return pd.read_csv(coupon_file)

# Function to save coupons to a CSV file
def save_coupons(coupons_df):
    coupons_df.to_csv(coupon_file, index=False)

# Function to create a new coupon
def create_coupon(coupon_code, discount, expiration_date):
    coupons_df = load_coupons()
    
    # Check if coupon already exists
    if coupon_code in coupons_df['Coupon Code'].values:
        st.error("Coupon code already exists!")
        return
    
    # Add the new coupon to the dataframe
    new_coupon = pd.DataFrame({
        "Coupon Code": [coupon_code],
        "Discount (%)": [discount],
        "Expiration Date": [expiration_date],
        "Active": [True],
        "Username": "all"  # Set the Username to 'all'

    })
    
    coupons_df = pd.concat([coupons_df, new_coupon], ignore_index=True)
    save_coupons(coupons_df)
    st.success(f"Coupon '{coupon_code}' created successfully!")
    st.rerun()

# Function to deactivate a coupon
def deactivate_coupon(coupon_code):
    coupons_df = load_coupons()
    if coupon_code in coupons_df['Coupon Code'].values:
        coupons_df.loc[coupons_df['Coupon Code'] == coupon_code, 'Active'] = False
        save_coupons(coupons_df)
        st.success(f"Coupon '{coupon_code}' deactivated successfully!")
        st.rerun()  # Rerun the app to update coupon status
    else:
        st.error("Coupon code not found!")

# Function to display and manage coupons
def display_promotions_page():
    st.title("Promotions & Discounts")
    
    # Show the existing coupons
    coupons_df = load_coupons()
    st.subheader("Existing Coupons")
    st.dataframe(coupons_df)
    
    # Create a new coupon
    st.subheader("Create New Coupon")
    coupon_code = st.text_input("Coupon Code")
    discount = st.number_input("Discount (%)", min_value=1, max_value=100, value=10)
    expiration_date = st.date_input("Expiration Date")
    
    if st.button("Create Coupon"):
        if coupon_code:
            create_coupon(coupon_code, discount, expiration_date)
        else:
            st.error("Please enter a coupon code.")
    
    # Deactivate a coupon
    st.subheader("Deactivate Coupon")
    deactivate_code = st.text_input("Coupon Code to Deactivate")
    
    if st.button("Deactivate Coupon"):
        if deactivate_code:
            deactivate_coupon(deactivate_code)
        else:
            st.error("Please enter a coupon code to deactivate.")