import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COVALENT_API_KEY")

wallet_df = pd.read_excel("wallets.xlsx")
wallets = wallet_df.iloc[:, 0].tolist()

compound_methods = {"borrow", "repayborrow", "mint", "redeem", "redeemunderlying", "liquidateborrow"}

def fetch_compound_transactions(wallet_address):
    url = f"https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/?key={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch data for {wallet_address} — Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return []

    txns = response.json().get("data", {}).get("items", [])
    compound_txns = []

    for tx in txns:
        log_events = tx.get("log_events", [])
        for log in log_events:
            decoded = log.get("decoded")
            if decoded and isinstance(decoded, dict):
                method = decoded.get("name", "").lower()
                if method in compound_methods:
                    compound_txns.append({
                        "wallet": wallet_address,
                        "tx_hash": tx.get("tx_hash"),
                        "method": method,
                        "value": tx.get("value"),
                        "gas_spent": tx.get("gas_spent"),
                        "timestamp": tx.get("block_signed_at")
                    })
                    break

    return compound_txns

if __name__ == "__main__":
    all_compound_data = []

    for wallet in wallets:
        print(f"🔍 Fetching Compound-related txns for: {wallet}")
        data = fetch_compound_transactions(wallet)
        if data:
            all_compound_data.extend(data)

    if all_compound_data:
        df = pd.DataFrame(all_compound_data)

        os.makedirs("data", exist_ok=True)
        df.to_csv("data/compound_transactions.csv", index=False)
        print(f"✅ Saved {len(df)} records to data/compound_transactions.csv")
    else:
        print("⚠️ No Compound transactions found across scanned wallets.")