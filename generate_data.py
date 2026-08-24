import pandas as pd
import random
from datetime import datetime, timedelta

# Make our random data reproducible
random.seed(42)

# Number of transactions to generate
number_of_transactions = 500


# Branches
branches = [
    "Kampala",
    "Entebbe",
    "Jinja"
]


# Products and their categories/prices
products = {
    "Smartphone": ("Electronics", 850000),
    "Headphones": ("Electronics", 120000),
    "Laptop Bag": ("Electronics", 85000),

    "Rice 5kg": ("Groceries", 32000),
    "Cooking Oil 3L": ("Groceries", 28000),
    "Sugar 2kg": ("Groceries", 12000),

    "Blender": ("Home & Kitchen", 180000),
    "Electric Kettle": ("Home & Kitchen", 95000),
    "Frying Pan": ("Home & Kitchen", 65000),

    "T-Shirt": ("Clothing", 45000),
    "Jeans": ("Clothing", 85000),
    "Jacket": ("Clothing", 150000),

    "Body Lotion": ("Personal Care", 25000),
    "Shampoo": ("Personal Care", 22000),
    "Toothpaste": ("Personal Care", 12000)
}


payment_methods = [
    "Cash",
    "Mobile Money",
    "Card"
]


customer_types = [
    "New",
    "Regular"
]


# Starting date
start_date = datetime(2026, 1, 1)


# Empty list where transactions will be stored
sales_data = []


# Generate transactions
for i in range(1, number_of_transactions + 1):

    product = random.choice(list(products.keys()))

    category = products[product][0]
    unit_price = products[product][1]

    transaction = {
        "Transaction_ID": f"TXN{i:04d}",
        "Date": start_date + timedelta(days=random.randint(0, 210)),
        "Branch": random.choice(branches),
        "Product": product,
        "Category": category,
        "Quantity": random.randint(1, 5),
        "Unit_Price": unit_price,
        "Payment_Method": random.choice(payment_methods),
        "Customer_Type": random.choice(customer_types)
    }

    sales_data.append(transaction)


# Convert list into a Pandas DataFrame
df = pd.DataFrame(sales_data)


# Sort transactions by date
df = df.sort_values("Date")


# Save to CSV
df.to_csv("data/sales_data.csv", index=False)


print("Sales dataset successfully created.")

print("\nFirst 5 records:")
print(df.head())