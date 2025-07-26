# 🛡️ Wallet Risk Scoring for Compound Protocol

This project implements a **behavior-based risk scoring system** for Ethereum wallets that interact with the Compound V2/V3 protocols.  
Each wallet is assigned a **risk score between 0 and 1000**, with **higher scores** representing responsible lending behavior and **lower scores** indicating risk-prone, bot-like, or exploitative usage.

---

## 🗂️ Project Structure
```powershell
compound-risk-scoring/
│
├── data/                   # Output CSVs and plots
│ ├── compound_transactions.csv
│ ├── compound_features.csv
│ ├── compound_risk_scores.csv
│ ├── score_distribution.png
│ └── analysis.md
│
├── src/                    # Modular codebase
│ ├── fetch_compound_data.py
│ ├── feature_engineering.py
│ ├── score_wallets.py
│ └── analyze_scores.py
│
├── wallets.xlsx            # Provided wallet addresses
├── main.py                 # One-click pipeline
├── .env                    # API key (excluded from Git)
├── requirements.txt        # Dependencies
└── README.md
```
---
## 🚀 How to Run

### 1️⃣ Setup
```powershell
# Clone the repo and enter the directory
git clone https://github.com/rushei1/compound-risk-scoring.git
cd compound-risk-scoring

# Set up virtual environment (PowerShell)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key in .env file
echo COVALENT_API_KEY=your_key_here > .env
```
### 2️⃣ Run the full pipeline
```powershell
python main.py
```
This will:
- Fetch Compound-related txns
- Generate features per wallet
- Compute risk scores
- Save output CSVs and score analysis plot
---
## 📥 Data Collection Method
- API: [CovalentHQ](https://www.covalenthq.com/docs/api/)
- Network: Ethereum Mainnet
- Scope: Only Compound-specific interactions (`borrow`, `repayBorrow`, `mint`, `redeem`, `redeemUnderlying`, `liquidateBorrow`)
- Filtering: Method names from decoded log_events per transaction
- 
---
## 🧠 Feature Engineering
| Feature              | Description                              |
| -------------------- | ---------------------------------------- |
| `tx_count`           | Total Compound transactions              |
| `total_gas`          | Total gas spent on Compound transactions |
| `total_value`        | Total transaction value                  |
| `borrow_count`       | Number of borrow calls                   |
| `repay_count`        | Number of repay calls                    |
| `mint_count`         | Number of mints (deposits)               |
| `redeem_count`       | Number of redeem calls                   |
| `liquidation_count`  | Times the wallet was liquidated          |
| `repay/borrow ratio` | Behavior indicator                       |
| `liquidation_ratio`  | Liquidations as a share of txs           |
---

## 📈 Scoring Logic (0–1000)
After normalization using `MinMaxScaler`, the risk score is computed as:

```powershell
score = (
    0.3 * repay_borrow_ratio +
    0.2 * mint_ratio +
    0.15 * tx_count_norm +
    0.15 * total_value_norm +
    0.10 * gas_norm +
    0.10 * (1 - liquidation_ratio)
) * 1000
```
This formula favors wallets that:
- Repay what they borrow
- Avoid frequent liquidation
- Have high volume/value interactions
- Show responsible, varied usage
---
## 📤 Output Format
`compound_risk_scores.csv`
| wallet                                     | risk\_score |
| ------------------------------------------ | ----------- |
| 0xfaa0768bde629806739c3a4620656c5d26f44ef2 | 732         |

Other Outputs:
- `compound_transactions_sample.csv` → raw txns
- `compound_features.csv` → engineered features
- `score_distribution.png` → histogram of wallet scores
- `analysis.md` → markdown-based insights
---

## 📊 Score Distribution

![Score Distribution](E:\Projects\Zeru_Assignment-2\compound-risk-scoring\data\score_distribution.png)
---
## ✍️ Risk Indicator Justification
| Metric                  | Interpretation         |
| ----------------------- | ---------------------- |
| High borrow + low repay | 🚩 High risk           |
| Frequent liquidations   | 🚩 High risk           |
| Mint + repay balance    | ✅ Healthy behavior     |
| High tx\_count + value  | ✅ Real user activity   |
| Gas usage               | Helps distinguish bots |
---

## 👨‍💻 Author
Rusheil Singh Baath  
B.Tech CSE (AI & Data Science)
