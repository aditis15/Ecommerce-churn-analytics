import pandas as pd

df = pd.read_csv("online_retail_II.csv", encoding="ISO-8859-1")

# Clean the data
df = df.dropna(subset=["Customer ID"])
df = df[df["Quantity"] > 0]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print(df.shape)

# Step 4: Build customer-level features
snapshot_date = df["InvoiceDate"].max()

customer_df = df.groupby("Customer ID").agg(
    last_purchase=("InvoiceDate", "max"),
    frequency=("Invoice", "nunique"),
    total_spend=("Price", "sum")
).reset_index()

customer_df["recency_days"] = (snapshot_date - customer_df["last_purchase"]).dt.days

print(customer_df.head())
print(customer_df.shape)
customer_df["churn_risk"] = customer_df["recency_days"].apply(
    lambda x: "High" if x > 90 else ("Medium" if x > 45 else "Low")
)

print(customer_df["churn_risk"].value_counts())
import sqlite3

conn = sqlite3.connect("ecommerce.db")
customer_df.to_sql("customers", conn, if_exists="replace", index=False)

# Example query: top 10 highest-spending high-risk customers
query = """
SELECT * FROM customers
WHERE churn_risk = 'High'
ORDER BY total_spend DESC
LIMIT 10
"""
high_risk = pd.read_sql(query, conn)
print(high_risk)
for _, row in high_risk.iterrows():
    message = f"Hi Customer {int(row['Customer ID'])}, we miss you! Here's 10% off your next order."
    print(message)
    