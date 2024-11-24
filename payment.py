import os
import random
import pandas as pd
import streamlit as st
import datetime
from fpdf import FPDF



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
def mark_coupon_as_used(coupon_code, file_path='coupons.csv'):
    if os.path.isfile(file_path):
        coupons_df = pd.read_csv(file_path)
        if coupon_code in coupons_df['Coupon Code'].values:
            coupons_df.loc[coupons_df['Coupon Code'] == coupon_code, 'Active'] = False
            coupons_df.to_csv(file_path, index=False)

# Function to generate a dummy invoice as a PDF
def generate_invoice(username, order_details, payment_method, branch, original_price, total_price):
    # Ensure the invoices folder exists
    invoice_folder = "invoices"
    if not os.path.exists(invoice_folder):
        os.makedirs(invoice_folder)
    
    # Define the invoice file path
    invoice_name = f"{invoice_folder}/invoice_{random.randint(1000, 9999)}.pdf"
    
    # Initialize FPDF instance
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    pdf.ln(10)
    
    # Add details to the PDF
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Username: {username}", ln=True)
    pdf.cell(0, 10, txt=f"Order Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, txt=f"Branch: {branch}", ln=True)
    pdf.cell(0, 10, txt=f"Payment Method: {payment_method}", ln=True)
    pdf.ln(10)

    # Order details
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, txt="Order Details:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in order_details.items():
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Display original price and discounted price
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, txt=f"Original Price: RM{original_price:.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Discounted Price: RM{total_price:.2f}", ln=True)
    pdf.ln(20)

    # Invoice footer
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Thank you for your purchase!", ln=True, align="C")
    
    # Save the PDF
    pdf.output(invoice_name)
    
    return invoice_name  # Return the valid path

def display_payment_page(username, order_details, total_price, branch, payment_method, booking_number, prep_time):
    st.title("Payment Page")
    st.write(f"Payment Method: **{payment_method}**")

    # Get the selected coupon from session state
    selected_coupon = order_details.get('Coupon', None)
    original_price = total_price  # Store the original price for invoice purposes
    
    if selected_coupon and selected_coupon != "No Coupons Available":
        # Load active coupons to check details
        active_coupons = load_active_coupons(username)
        discount_row = active_coupons[active_coupons['Coupon Code'] == selected_coupon]

        if not discount_row.empty:
            # Coupon is valid, apply discount
            discount_percentage = discount_row['Discount (%)'].values[0]
            total_price *= (1 - discount_percentage / 100)

            st.write(f"Coupon `{selected_coupon}` applied! Discount: {discount_percentage}%")
            st.write(f"**Original Price:** RM{original_price:.2f}")
            st.write(f"**Price After Discount:** RM{total_price:.2f}")
            


    else:
        st.write("No coupon applied.")
        st.write(f"**Total Price:** RM{total_price:.2f}")

    # If the payment method is FPX, show the bank selection dropdown
    if payment_method == "FPX":
        st.write("Please select your bank to proceed with FPX payment:")
        banks = [
            "Maybank", "CIMB", "Public Bank", "RHB Bank", "Hong Leong Bank",
            "Affin Bank", "UOB", "Bank Islam", "Bank Rakyat", "Standard Chartered"
        ]
        selected_bank = st.selectbox("Select Bank", banks)

        if selected_bank:
            st.write(f"You have selected: {selected_bank}")

    # Add the "Pay Now" button
    if st.button("Pay Now"):
        # Mark coupon as used
        mark_coupon_as_used(selected_coupon)
        # Simulate successful payment process
        st.success("Payment successful! Your order has been processed.")
        st.success(f"Order placed! Your booking number is {booking_number}. Estimated preparation time is {prep_time} minutes.")

        # Generate the invoice with both original and discounted prices
    invoice_path = generate_invoice(username, order_details, payment_method, branch, original_price, total_price)

        # Provide option to download the invoice
    with open(invoice_path, "rb") as file:
            st.download_button(
                label="Download Invoice",
                data=file,
                file_name=os.path.basename(invoice_path),
                mime="application/pdf"
            )

    # Button to go back to homepage
    if st.button("Go back to Main Page"):
        st.session_state["page"] = "Homepage"
        st.rerun()
