import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
# Load the dataset
df = pd.read_csv("sales_data.csv")

# Display first 5 rows
print(df.head())
# Check for missing values
print(df.isnull().sum())

# Fill missing values with appropriate strategies
df["category"] = df["category"].fillna("Unknown")
df["total_sales"] = df["total_sales"].fillna(df["quantity"] * df["price"])

df.dropna(inplace=True)  # Drop rows with critical missing data
# Ensure order_date is in the correct format (YYYY-MM-DD)
df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

# Connect to SQLite database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        order_id INTEGER PRIMARY KEY,
        product TEXT,
        category TEXT,
        quantity INTEGER,
        price REAL,
        total_sales REAL,
        order_date TEXT,
        customer_id INTEGER,
        region TEXT
    )
''')
# Read sales data from CSV
df = pd.read_csv("sales_data.csv")

# Insert data into the SQLite database
df.to_sql("sales", conn, if_exists="replace", index=False)
print("Data stored in SQLite successfully!")

# SQL Query for total revenue
query = "SELECT SUM(total_sales) AS total_revenue FROM sales"
total_revenue = pd.read_sql(query, conn)
print(total_revenue)

query = """
    SELECT product, SUM(quantity) AS total_sold 
    FROM sales 
    GROUP BY product 
    ORDER BY total_sold DESC 
    LIMIT 5
"""
top_products = pd.read_sql(query, conn)
print(top_products)
# SQL Query for monthly revenue
query = """
    SELECT strftime('%Y-%m', order_date) AS month, SUM(total_sales) AS revenue 
    FROM sales 
    GROUP BY month 
    ORDER BY month;
"""
monthly_revenue = pd.read_sql(query, conn)
print(monthly_revenue)
# Average sales per order
avg_sales = np.mean(df["total_sales"])
print(f"Average Sales per Order: ${avg_sales:.2f}")

# Median sales per order
median_sales = np.median(df["total_sales"])
print(f"Median Sales per Order: ${median_sales:.2f}")

# Standard deviation of sales
std_dev_sales = np.std(df["total_sales"])
print(f"Sales Standard Deviation: ${std_dev_sales:.2f}")
# Group by region and sum total sales
region_sales = df.groupby("region")["total_sales"].sum().reset_index()

# Sort and display top region
best_region = region_sales.sort_values(by="total_sales", ascending=False).iloc[0]
print(f"Best Performing Region: {best_region['region']} with revenue ${best_region['total_sales']:.2f}")

# Group by month
df["month"] = pd.to_datetime(df["order_date"]).dt.to_period("M")
monthly_sales = df.groupby("month")["total_sales"].sum()

# Plot monthly sales trend
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', linestyle='-')
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.grid()
plt.show()
# Plot Top 5 Best-Selling Products
plt.figure(figsize=(8, 5))
plt.bar(top_products["product"], top_products["total_sold"], color="skyblue")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.title("Top 5 Best-Selling Products")
plt.xticks(rotation=45)
plt.show()
# Plot Sales Distribution
plt.figure(figsize=(8, 5))
plt.hist(df["total_sales"], bins=20, color="orange", edgecolor="black")
plt.xlabel("Total Sales per Order")
plt.ylabel("Frequency")
plt.title("Sales Distribution")
plt.show()

conn.commit()
conn.close()
print("Database connection closed.")
