import argparse
import os
import random
import uuid
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

PRODUCTS = [
    ("P001", "Laptop",       "Electronics", 45000, 120000),
    ("P002", "Headphones",   "Electronics",   800,   5000),
    ("P003", "T-Shirt",      "Apparel",        299,   2500),
    ("P004", "Running Shoes","Footwear",      1500,   8000),
    ("P005", "Coffee Maker", "Appliances",    1200,   6000),
    ("P006", "Novel",        "Books",          150,    800),
    ("P007", "Backpack",     "Accessories",    800,   4000),
    ("P008", "Yoga Mat",     "Sports",         500,   2000),
]

REGIONS         = ["North", "South", "East", "West", "Central"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"]
STATUSES        = ["Completed", "Shipped", "Processing", "Cancelled", "Returned"]


def generate_orders(n_rows=10_000, anomaly_pct=0.06, seed=42):
    rng = np.random.default_rng(seed)
    random.seed(seed)

    n_anomaly = int(n_rows * anomaly_pct)
    n_clean   = n_rows - n_anomaly
    records   = []
    base_date = datetime(2024, 1, 1)

    # Clean records
    for _ in range(n_clean):
        prod  = random.choice(PRODUCTS)
        qty   = int(rng.integers(1, 6))
        price = round(float(rng.uniform(prod[3], prod[4])), 2)
        odate = base_date + timedelta(days=int(rng.integers(0, 365)))
        records.append({
            "order_id":       str(uuid.uuid4()),
            "customer_id":    f"CUST{rng.integers(1000,9999):04d}",
            "product_id":     prod[0],
            "product_name":   prod[1],
            "category":       prod[2],
            "quantity":       qty,
            "unit_price":     price,
            "total_amount":   round(price * qty, 2),
            "order_date":     odate.strftime("%Y-%m-%d %H:%M:%S"),
            "region":         random.choice(REGIONS),
            "payment_method": random.choice(PAYMENT_METHODS),
            "status":         random.choice(STATUSES),
            "discount_pct":   round(float(rng.uniform(0, 0.30)), 3),
        })

    # Anomaly records
    anomaly_types = ["null_spike", "price_outlier", "future_date",
                     "duplicate", "zero_amount"]
    for _ in range(n_anomaly):
        atype = random.choice(anomaly_types)
        prod  = random.choice(PRODUCTS)
        qty   = int(rng.integers(1, 4))
        price = round(float(rng.uniform(prod[3], prod[4])), 2)
        odate = base_date + timedelta(days=int(rng.integers(0, 365)))

        record = {
            "order_id":       str(uuid.uuid4()),
            "customer_id":    f"CUST{rng.integers(1000,9999):04d}",
            "product_id":     prod[0],
            "product_name":   prod[1],
            "category":       prod[2],
            "quantity":       qty,
            "unit_price":     price,
            "total_amount":   round(price * qty, 2),
            "order_date":     odate.strftime("%Y-%m-%d %H:%M:%S"),
            "region":         random.choice(REGIONS),
            "payment_method": random.choice(PAYMENT_METHODS),
            "status":         random.choice(STATUSES),
            "discount_pct":   round(float(rng.uniform(0, 0.30)), 3),
        }

        if atype == "null_spike":
            for f in random.sample(
                ["customer_id","product_id","region","payment_method"], 2):
                record[f] = None

        elif atype == "price_outlier":
            record["unit_price"]   = round(price * random.uniform(10, 50), 2)
            record["total_amount"] = round(record["unit_price"] * qty, 2)

        elif atype == "future_date":
            future = datetime.now() + timedelta(days=random.randint(30, 365))
            record["order_date"] = future.strftime("%Y-%m-%d %H:%M:%S")

        elif atype == "duplicate":
            if records:
                record["order_id"] = random.choice(records)["order_id"]

        elif atype == "zero_amount":
            record["total_amount"] = 0.0
            record["unit_price"]   = 0.0

        records.append(record)

    df = pd.DataFrame(records).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


def save(df, output_dir, filename="orders_raw.csv"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"Saved {len(df):,} rows → {path}")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows",        type=int,   default=10_000)
    parser.add_argument("--anomaly-pct", type=float, default=0.06)
    parser.add_argument("--output-dir",  default="data/raw")
    args = parser.parse_args()

    df = generate_orders(n_rows=args.rows, anomaly_pct=args.anomaly_pct)
    save(df, args.output_dir)