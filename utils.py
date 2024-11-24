import os
import pandas as pd

inventory_file = 'inventory.csv'

# Load inventory from CSV
if os.path.isfile(inventory_file):
    # Read the CSV and convert the item names to a normalized format (e.g., removing spaces)
    inventory_data = pd.read_csv(inventory_file)
    inventory = {item.strip().replace(' ', '_').lower(): amount for item, amount in zip(inventory_data['Item'], inventory_data['Amount'])}
else:
    inventory = {}

max_stock = {
    'coffee_beans': 1000,
    'milk': 500,
    'sugar': 200,
    'cups': 50
}

# Save inventory back to CSV
def save_inventory(inventory_data):
    # Convert the inventory dictionary back to a DataFrame
    df = pd.DataFrame(list(inventory_data.items()), columns=['Item', 'Amount'])
    # Adjust item names for display (e.g., replace underscores with spaces)
    df['Item'] = df['Item'].str.replace('_', ' ').str.title()
    df.to_csv(inventory_file, index=False)

# Check low inventory items
def check_low_inventory(inventory):
    low_inventory = {}
    for item, amount in inventory.items():
        # Check if current amount is less than 20% of max stock
        if amount < 0.2 * max_stock.get(item, 0):
            low_inventory[item] = amount
    return low_inventory
