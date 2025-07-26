import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/compound_risk_scores.csv")

score_col = "risk_score"

os.makedirs("data", exist_ok=True)

plt.figure(figsize=(10, 6))
bins = [i for i in range(0, 1100, 100)]
plt.hist(df[score_col], bins=bins, color="skyblue", edgecolor="black")
plt.title("Risk Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("Number of Wallets")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/score_distribution.png")
plt.close()

score_ranges = [(0, 100), (100, 200), (200, 400), (400, 600), (600, 800), (800, 1000)]
descriptions = [
    "🚨 Extremely high-risk: very low interaction or unhealthy usage",
    "⚠️ High-risk: rare repays, or suspicious interactions",
    "🟠 Mid risk: low diversity, uncertain patterns",
    "🟡 Moderate: some diversity, not highly active",
    "🟢 Low risk: reliable, decent behavior",
    "✅ Very reliable: active, consistent repay, no signs of exploit"
]

with open("data/analysis.md", "w", encoding="utf-8") as f:
    f.write("# 📊 Compound Wallet Risk Analysis\n\n")
    f.write("## 🔢 Score Distribution:\n\n")
    f.write("![Risk Histogram](score_distribution.png)\n\n")
    f.write("| Score Range | Wallets | Risk Interpretation |\n")
    f.write("|-------------|---------|----------------------|\n")

    for (low, high), desc in zip(score_ranges, descriptions):
        count = df[(df[score_col] >= low) & (df[score_col] < high)].shape[0]
        f.write(f"| {low}-{high} | {count} | {desc} |\n")

print("✅ analysis.md and score_distribution.png generated in 'data/' folder.")