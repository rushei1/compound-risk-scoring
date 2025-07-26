import pandas as pd
import os

df = pd.read_csv("data/compound_transactions.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

compound_methods = ["borrow", "repayborrow", "mint", "redeem", "redeemunderlying", "liquidateborrow"]

onehot = pd.get_dummies(df["method"])
for method in compound_methods:
    if method not in onehot.columns:
        onehot[method] = 0

df = pd.concat([df, onehot], axis=1)

features = df.groupby("wallet").agg({
    "tx_hash": "count",
    "gas_spent": "sum",
    "timestamp": lambda x: (x.max() - x.min()).total_seconds() / (len(x)-1) if len(x) > 1 else 0,
    "mint": "sum",
    "redeem": "sum",
    "borrow": "sum",
    "repayborrow": "sum",
    "liquidateborrow": "sum"
}).reset_index()

features.rename(columns={
    "tx_hash": "tx_count",
    "gas_spent": "total_gas_spent",
    "timestamp": "avg_tx_gap",
    "repayborrow": "repay_count",
    "borrow": "borrow_count",
    "mint": "mint_count",
    "redeem": "redeem_count",
    "liquidateborrow": "liquidate_count"
}, inplace=True)

features["repay_borrow_ratio"] = features["repay_count"] / features["borrow_count"].replace(0, 1)

os.makedirs("data", exist_ok=True)
features.to_csv("data/compound_features.csv", index=False)
print("✅ Features saved to data/compound_features.csv")