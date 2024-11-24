import os
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import save_inventory, check_low_inventory, max_stock, inventory

orders_file = 'orders.csv'

# Load orders from the CSV file
def load_orders():
    if os.path.isfile(orders_file):
        return pd.read_csv(orders_file, parse_dates=['Order Time'])
    return pd.DataFrame()  # Empty dataframe if no orders found

# Custom function to render a progress bar with color
def colored_progress_bar(ratio, color):
    """ Renders a colored progress bar using HTML and CSS """
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; border-radius: 5px; width: 100%; height: 20px;">
            <div style="background-color: {color}; width: {ratio * 100}%; height: 100%; border-radius: 5px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_analytics_dashboard():
    st.title("Analytics Dashboard")

    # Radio button for page selection
    page_option = st.radio("Choose Report Type", ['Sales Trends', 'Inventory Health', 'Order Management'])

    # Load the order data
    orders_df = load_orders()
    
    if orders_df.empty:
        st.info("No sales data found. Please add orders to view analytics.")
        return

    # Display the appropriate section based on page option
    if page_option == 'Sales Trends':
        st.subheader("Sales Trends")

        # Get current date and time data
        today = datetime.today().date()
        orders_df['Hour'] = orders_df['Order Time'].dt.hour
        orders_df['Date'] = orders_df['Order Time'].dt.date
        orders_df['Week'] = orders_df['Order Time'].dt.to_period('W')
        orders_df['Month'] = orders_df['Order Time'].dt.to_period('M')

        # User selects grouping option for the sales data
        group_option = st.selectbox("Select Grouping", ['Hourly', 'Daily', 'Weekly', 'Monthly'])

        if group_option == 'Hourly':
            # Group by Hour
            sales_by_hour = orders_df.groupby('Hour').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
            st.subheader("Sales Trend (Hourly)")
            st.write(f"**Hourly Sales**: Total Revenue Today: RM {sales_by_hour['Revenue'].sum():,.2f}")
            st.dataframe(sales_by_hour)
            st.line_chart(sales_by_hour)

        elif group_option == 'Daily':
            # Group by Date
            sales_by_date = orders_df.groupby('Date').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
            st.subheader("Sales Trend (Daily)")
            st.write(f"**Daily Sales**: Total Revenue Today: RM {sales_by_date['Revenue'].sum():,.2f}")
            st.dataframe(sales_by_date)
            st.line_chart(sales_by_date)

        elif group_option == 'Weekly':
            # Group by Week
            sales_by_week = orders_df.groupby('Week').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
            st.subheader("Sales Trend (Weekly)")
            st.write(f"**Weekly Sales**: Total Revenue: RM {sales_by_week['Revenue'].sum():,.2f}")
            st.dataframe(sales_by_week)
            st.line_chart(sales_by_week['Revenue'])

        elif group_option == 'Monthly':
            # Group by Month
            sales_by_month = orders_df.groupby('Month').agg(Quantity=('Price', 'count'), Revenue=('Price', 'sum'))
            st.subheader("Sales Trend (Monthly)")
            st.write(f"**Monthly Sales**: Total Revenue: RM {sales_by_month['Revenue'].sum():,.2f}")
            st.dataframe(sales_by_month)
            st.line_chart(sales_by_month['Revenue'])

    elif page_option == 'Inventory Health':
        st.subheader("Inventory Health Check")
        low_inventory_items = check_low_inventory(inventory)
        
        if low_inventory_items:
            st.warning(f"The following items are running low and need restocking: {', '.join(low_inventory_items)}")
        else:
            st.success("All inventory levels are healthy.")

        # Show Current Inventory Levels
        with st.expander("Current Inventory Levels", expanded=True):
            st.subheader("Inventory Levels")

            for item, amount in inventory.items():
                max_amount = max_stock.get(item, 0)
                stock_ratio = min(amount / max_amount, 1.0) if max_amount else 0  # Avoid division by zero
                status = "Low Stock" if stock_ratio <= 0.2 else "Medium Stock" if stock_ratio <= 0.5 else "High Stock"
                
                # Color logic for progress bar
                color = 'red' if stock_ratio <= 0.2 else 'orange' if stock_ratio <= 0.5 else 'green'
                st.write(f"**{item.capitalize()}**: {amount}/{max_amount} ({status})")
                
                # Displaying the colored progress bar
                colored_progress_bar(stock_ratio, color)

    elif page_option == 'Order Management':
        st.subheader("Real-Time Orders")
        
        # Filter Orders based on user input for order status
        order_status = st.selectbox("Select Order Status", ['All', 'Preparing', 'Ready for Pickup', 'Done'])
        
        # Filter by Branch
        branch = st.selectbox("Select Branch", ['All'] + list(orders_df['Branch'].unique()))  # 'All' allows to view orders from all branches
        
        # Apply filters
        if order_status == 'All' and branch == 'All':
            filtered_orders = orders_df  # No filtering, show all orders
        elif order_status == 'All':
            filtered_orders = orders_df[orders_df['Branch'] == branch]  # Filter by branch only
        elif branch == 'All':
            filtered_orders = orders_df[orders_df['Status'] == order_status]  # Filter by status only
        else:
            filtered_orders = orders_df[(orders_df['Status'] == order_status) & (orders_df['Branch'] == branch)]  # Filter by both

        if filtered_orders.empty:
            st.info(f"No orders found with status: {order_status} and branch: {branch}")
        else:
            st.dataframe(filtered_orders[['Order Time', 'Coffee Type', 'Price', 'Status', 'Branch']])
