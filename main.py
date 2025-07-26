import subprocess
import sys

print("Step 1: Fetching transaction data from Covalent...")
subprocess.run([sys.executable, "src/fetch_compound_data.py"], check=True)

print("Step 2: Extracting features...")
subprocess.run([sys.executable, "src/feature_engineering.py"], check=True)

print("Step 3: Scoring wallets...")
subprocess.run([sys.executable, "src/score_wallets.py"], check=True)

print("Step 4: Generating analysis...")
subprocess.run([sys.executable, "src/analyze_scores.py"], check=True)

print("✅ Pipeline completed successfully!")
