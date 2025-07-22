import pandas as pd
import sqlite3
import os

def load_to_sqlite():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/ecommerce.db")

    df1 = pd.read_csv("data/ad_sales_metrics.csv")
    df2 = pd.read_csv("data/total_sales_metrics.csv")
    df3 = pd.read_csv("data/product_eligibility.csv")

    df1.to_sql("ad_sales_metrics", conn, if_exists="replace", index=False)
    df2.to_sql("total_sales_metrics", conn, if_exists="replace", index=False)
    df3.to_sql("product_eligibility", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    load_to_sqlite()
