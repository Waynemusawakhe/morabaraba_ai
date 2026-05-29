# ============================================
# graphs.py
# Generate training graphs
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

TRAINING_CSV = "results/training_data.csv"

if not os.path.exists(TRAINING_CSV):
    print("No training data found. Run train.py first to generate results.")
    sys.exit(1)

# ============================================
# Load training data
# ============================================

data = pd.read_csv(TRAINING_CSV)

# create graphs folder
os.makedirs("results/graphs", exist_ok=True)

# ============================================
# GRAPH 1 — Epsilon Decay
# ============================================

plt.figure(figsize=(10,5))

plt.plot(data["episode"], data["epsilon"])

plt.title("Epsilon Decay Over Time")
plt.xlabel("Episode")
plt.ylabel("Epsilon")

plt.grid(True)

plt.savefig("results/graphs/epsilon_decay.png")

print("Saved epsilon_decay.png")

# ============================================
# GRAPH 2 — Win Distribution
# ============================================

winner_counts = data["winner"].value_counts()

plt.figure(figsize=(6,6))

winner_counts.plot(kind="bar")

plt.title("Win Distribution")
plt.xlabel("Player")
plt.ylabel("Wins")

plt.grid(True)

plt.savefig("results/graphs/win_distribution.png")

print("Saved win_distribution.png")

# ============================================
# GRAPH 3 — Rolling Win Rate
# ============================================

data["player1_win"] = (data["winner"] == 1).astype(int)

rolling_winrate = data["player1_win"].rolling(100).mean()

plt.figure(figsize=(10,5))

plt.plot(data["episode"], rolling_winrate)

plt.title("Rolling Win Rate (Player 1)")
plt.xlabel("Episode")
plt.ylabel("Win Rate")

plt.grid(True)

plt.savefig("results/graphs/rolling_winrate.png")

print("Saved rolling_winrate.png")

# ============================================
# DONE
# ============================================

print("\nGraphs generated successfully.")