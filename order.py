import random
import streamlit as st
import pandas as pd
import datetime
import os
from PIL import Image
from payment import display_payment_page

# Function to load and filter active coupons
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

# Function to save orders to CSV
def save_order_to_csv(order):
    if not os.path.isfile('orders.csv'):
        df = pd.DataFrame([order])
        df.to_csv('orders.csv', index=False)
    else:
        df = pd.DataFrame([order])
        df.to_csv('orders.csv', mode='a', header=False, index=False)

# Function to resize images
def resize_image(image_path, size=(150, 150)):
    image = Image.open(image_path)
    return image.resize(size)


# Function to display the order page
def display_order_page(username):
    st.title(f"Welcome, {username}!")
    st.header("Menu")

    # Coffee menu with prices and images
    menu = {
        'Americano': {
            'price': 6.00,
            'image': 'americano.jpg'
        },
        'Cappuccino': {
            'price': 7.00,
            'image': 'cappucino.jpg'
        },
        'Latte': {
            'price': 7.50,
            'image': 'latte.jpg'
        },
        'Caramel Macchiato': {
            'price': 8.00,
            'image': 'caramel.jpg'
        }
    }

    # Display the menu with resized images
    cols = st.columns(len(menu))
    for idx, (coffee_type, details) in enumerate(menu.items()):
        with cols[idx]:
            resized_image = resize_image(details['image'])
            st.image(resized_image, caption=coffee_type)
            st.write(f"Price: RM{details['price']:.2f}")

    # Branch Selection Dropdown
    branches = ['Seri Iskandar', 'Ipoh', 'Manjung']
    selected_branch = st.selectbox("Select Branch", branches)
    st.write(f"**Selected Branch:** {selected_branch}")

    # Load active coupons
    active_coupons = load_active_coupons(username)
    if not active_coupons.empty:
        coupon_options = active_coupons['Coupon Code'].tolist()
    else:
        coupon_options = ["No Coupons Available"]

    # Order placement form
    with st.form(key='order_form'):
        coffee_type = st.selectbox("Select Coffee", list(menu.keys()))
        size = st.radio("Select Size", ['Small', 'Medium', 'Large'])
        ice = st.radio("Choice of Ice", ['Hot', 'Less', 'Normal'])
        sugar = st.radio("Choice of Sugar", ['No', 'Less', 'Normal'])
        add_ons = st.multiselect("Add-ons", ['Milk', 'Whipped Cream', 'Extra Shot'])

        # Coupon selection
        selected_coupon = st.selectbox("Choose Coupon (Optional)", coupon_options)

        # Payment method selection
        payment_method = st.radio("Select Payment Method", ["FPX", "Credit/Debit Card", "E-Wallet"])
        
        submit_order = st.form_submit_button("Place Order")

        if submit_order:
            # Calculate base price
            price = menu[coffee_type]['price']

            # Generate other order details
            booking_number = str(random.randint(1000, 9999))
            prep_time = random.randint(5, 15)  # Random prep time between 5 to 15 minutes
            order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            order = {
                'Username': username,
                'Coffee Type': coffee_type,
                'Size': size,
                'Ice': ice,
                'Sugar': sugar,
                'Add-ons': ', '.join(add_ons),
                'Price (RM)': f"{price:.2f}",  # Base price without discount
                'Booking Number': booking_number,
                'Preparation Time (min)': prep_time,
                'Order Time': order_time,
                'Branch': selected_branch,
                'Status': 'Preparing',
                'Payment Method': payment_method,
                'Coupon':selected_coupon
                
            }

            # Save the order to CSV
            save_order_to_csv(order)

            # Store order details in session state
            st.session_state.order = order

            # Redirect to Payment Page
            st.session_state.page = "payment"
            st.rerun()
