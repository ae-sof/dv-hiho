import os
import pandas as pd
import streamlit as st
import altair as alt

# Assuming inventory costs for simplicity
coffee_costs = {
    'Americano': 3.0,  # Cost per unit for Americano
    'Cappuccino': 3.5,  # Cost per unit for Cappuccino
    'Latte': 4.5,       # Cost per unit for Latte
    'Caramel Macchiato': 4.5  # Cost per unit for CM
}

orders_file = 'orders.csv'

def display_sales_reporting():  
    st.title("Sales Reporting")
    
    if not os.path.isfile(orders_file):
        st.info("No sales data found. Please add orders to view reports.")
        return

    # Load Orders Data
    orders_df = pd.read_csv(orders_file, parse_dates=['Order Time'])

    # Adding date-based columns for grouping
    orders_df['Date'] = orders_df['Order Time'].dt.date
    orders_df['Week'] = orders_df['Order Time'].dt.to_period('W').dt.start_time
    orders_df['Month'] = orders_df['Order Time'].dt.to_period('M').dt.start_time

    # Select box for choosing the report type
    report_type = st.selectbox(
        "Select Report Type",
        ["Total Sales Report", "Sales Breakdown by Coffee Type", "Best and Worst Sellers", "Total Profit Calculation"]
    )

    if report_type == "Total Sales Report":
        # Group by Date for Daily Sales Report
        daily_sales = orders_df.groupby('Date').agg(
            Quantity=('Price', 'count'),
            Revenue=('Price', 'sum')
        ).reset_index()

        daily_sales_melted = daily_sales.melt(id_vars=['Date'], value_vars=['Revenue', 'Quantity'],
                                              var_name='Metric', value_name='Value')

        st.write("### Daily Sales")
        daily_sales_chart = alt.Chart(daily_sales_melted).mark_line().encode(
            x='Date:T',
            y='Value:Q',
            color='Metric:N',  # This will generate the legend
            tooltip=['Date:T', 'Metric:N', 'Value:Q'],  # Tooltip for hover
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(daily_sales_chart, use_container_width=True)
        st.write(daily_sales)  # Display the dataframe below the chart

        # Weekly Sales
        weekly_sales = orders_df.groupby('Week').agg(
            Quantity=('Price', 'count'),
            Revenue=('Price', 'sum')
        ).reset_index()

        weekly_sales_melted = weekly_sales.melt(id_vars=['Week'], value_vars=['Revenue', 'Quantity'],
                                                var_name='Metric', value_name='Value')

        st.write("### Weekly Sales")
        weekly_sales_chart = alt.Chart(weekly_sales_melted).mark_line().encode(
            x='Week:T',
            y='Value:Q',
            color='Metric:N',
            tooltip=['Week:T', 'Metric:N', 'Value:Q'],
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(weekly_sales_chart, use_container_width=True)
        st.write(weekly_sales)  # Display the dataframe below the chart

        # Monthly Sales
        monthly_sales = orders_df.groupby('Month').agg(
            Quantity=('Price', 'count'),
            Revenue=('Price', 'sum')
        ).reset_index()

        monthly_sales_melted = monthly_sales.melt(id_vars=['Month'], value_vars=['Revenue', 'Quantity'],
                                                  var_name='Metric', value_name='Value')

        st.write("### Monthly Sales")
        monthly_sales_chart = alt.Chart(monthly_sales_melted).mark_line().encode(
            x='Month:T',
            y='Value:Q',
            color='Metric:N',
            tooltip=['Month:T', 'Metric:N', 'Value:Q'],
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(monthly_sales_chart, use_container_width=True)
        st.write(monthly_sales)  # Display the dataframe below the chart

    elif report_type == "Sales Breakdown by Coffee Type":
        # Group by Coffee Type for sales breakdown
        coffee_breakdown = orders_df.groupby('Coffee Type').agg(
            Quantity=('Price', 'count'),
            Revenue=('Price', 'sum')
        ).reset_index().sort_values('Quantity', ascending=False)

        st.write("### Coffee Type Breakdown")
        coffee_type_chart = alt.Chart(coffee_breakdown).mark_bar().encode(
            x='Quantity:Q',
            y='Coffee Type:N',
            color='Coffee Type:N',
            tooltip=['Coffee Type:N', 'Quantity:Q', 'Revenue:Q']
        ).properties(width=700, height=400).interactive()

        st.altair_chart(coffee_type_chart, use_container_width=True)
        st.write(coffee_breakdown)  # Display the dataframe below the chart

    elif report_type == "Best and Worst Sellers":
        # Group by Coffee Type for best and worst sellers
        coffee_sales = orders_df.groupby('Coffee Type').agg(
            Quantity=('Price', 'count'),
            Revenue=('Price', 'sum')
        ).reset_index()

        # Find the best seller (highest quantity) and worst seller (lowest quantity)
        best_seller = coffee_sales.loc[coffee_sales['Quantity'].idxmax()]
        worst_seller = coffee_sales.loc[coffee_sales['Quantity'].idxmin()]

        st.write("### Best and Worst Sellers")
        
        # Display Best and Worst Sellers Text Information
        st.write(f"**Best-selling coffee type**: {best_seller['Coffee Type']} with {best_seller['Quantity']} sold")
        st.write(f"**Worst-selling coffee type**: {worst_seller['Coffee Type']} with {worst_seller['Quantity']} sold")
        
        # Bar Chart showing Coffee Sales to visualize Best and Worst Sellers
        coffee_sales_sorted = coffee_sales.sort_values('Quantity', ascending=False)

        coffee_sales_chart = alt.Chart(coffee_sales_sorted).mark_bar().encode(
            x='Quantity:Q',
            y='Coffee Type:N',
            color='Coffee Type:N',
            tooltip=['Coffee Type:N', 'Quantity:Q', 'Revenue:Q']
        ).properties(width=700, height=400).interactive()

        st.altair_chart(coffee_sales_chart, use_container_width=True)
        st.write(coffee_sales_sorted)  # Display the dataframe below the chart

    elif report_type == "Total Profit Calculation":
        # Calculate profit: Revenue - Cost
        orders_df['Cost'] = orders_df['Coffee Type'].map(coffee_costs)
        orders_df['Profit'] = orders_df['Price'] - orders_df['Cost']

        # Group by Date for Daily Profit
        daily_profit = orders_df.groupby('Date')['Profit'].sum().reset_index()
        st.write("### Daily Profit")
        daily_profit_chart = alt.Chart(daily_profit).mark_line().encode(
            x='Date:T',
            y='Profit:Q',
            color=alt.value('green'),
            tooltip=['Date:T', 'Profit:Q'],
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(daily_profit_chart, use_container_width=True)
        st.write(daily_profit)  # Display the dataframe below the chart

        # Weekly Profit
        weekly_profit = orders_df.groupby('Week')['Profit'].sum().reset_index()
        st.write("### Weekly Profit")
        weekly_profit_chart = alt.Chart(weekly_profit).mark_line().encode(
            x='Week:T',
            y='Profit:Q',
            color=alt.value('green'),
            tooltip=['Week:T', 'Profit:Q'],
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(weekly_profit_chart, use_container_width=True)
        st.write(weekly_profit)  # Display the dataframe below the chart

        # Monthly Profit
        monthly_profit = orders_df.groupby('Month')['Profit'].sum().reset_index()
        st.write("### Monthly Profit")
        monthly_profit_chart = alt.Chart(monthly_profit).mark_line().encode(
            x='Month:T',
            y='Profit:Q',
            color=alt.value('green'),
            tooltip=['Month:T', 'Profit:Q'],
            size=alt.value(3)
        ).properties(width=700, height=400).interactive()

        st.altair_chart(monthly_profit_chart, use_container_width=True)
        st.write(monthly_profit)  # Display the dataframe below the chart
