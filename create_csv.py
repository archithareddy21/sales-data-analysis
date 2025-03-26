import pandas as pd

# Create sample sales data
data = {
    "order_id": [1, 2, 3, 4, 5],
    "product": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "category": ["Electronics", "Electronics", "Accessories", "Accessories", "Electronics"],
    "quantity": [2, 1, 3, 2, 1],
    "price": [500, 1200, 150, 200, 800],
    "total_sales": [1000, 1200, 450, 400, 800],
    "order_date": ["2024-01-10", "2024-01-12", "2024-02-05", "2024-02-07", "2024-02-10"],
    "customer_id": [101, 102, 103, 104, 105],
    "region": ["North", "West", "East", "South", "North"]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Save as CSV
df.to_csv("sales_data.csv", index=False)

print("CSV file created successfully!")
