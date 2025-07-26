import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

df = pd.read_csv("data/compound_features.csv")

df.fillna(0, inplace=True)

df["liquidation_ratio"] = df["liquidate_count"] / df["tx_count"]
df["mint_redeem_activity"] = df["mint_count"] + df["redeem_count"]

scaler = MinMaxScaler()
df_norm = scaler.fit_transform(df[[
    "repay_borrow_ratio",
    "liquidation_ratio",
    "tx_count",
    "mint_redeem_activity",
    "avg_tx_gap"
]])

df_norm = pd.DataFrame(df_norm, columns=[
    "repay_borrow_ratio", 
    "liquidation_ratio", 
    "tx_count", 
    "mint_redeem_activity", 
    "avg_tx_gap"
])
df_norm["liquidation_ratio"] = 1 - df_norm["liquidation_ratio"]
df_norm["avg_tx_gap"] = 1 - df_norm["avg_tx_gap"]

df["risk_score"] = (
    0.3 * df_norm["repay_borrow_ratio"] +
    0.2 * df_norm["liquidation_ratio"] +
    0.2 * df_norm["tx_count"] +
    0.15 * df_norm["mint_redeem_activity"] +
    0.15 * df_norm["avg_tx_gap"]
)
df["risk_score"] = (df["risk_score"] * 1000).round(0).astype(int)

os.makedirs("data", exist_ok=True)
df[["wallet", "risk_score"]].to_csv("data/compound_risk_scores.csv", index=False)
print("✅ Risk scores saved to data/compound_risk_scores.csv")