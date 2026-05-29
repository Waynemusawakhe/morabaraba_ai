# ============================================
# metrics.py
# Training statistics summary
# ============================================

import pandas as pd
import pickle
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

# ============================================
# Basic statistics
# ============================================

total_games = len(data)

player1_wins = (data["winner"] == 1).sum()
player2_wins = (data["winner"] == -1).sum()

player1_rate = (player1_wins / total_games) * 100
player2_rate = (player2_wins / total_games) * 100

final_epsilon = data["epsilon"].iloc[-1]

# ============================================
# Load Q-table size
# ============================================

qtable_size = 0

if os.path.exists("results/qtable.pkl"):

    with open("results/qtable.pkl", "rb") as file:

        q_table = pickle.load(file)

        qtable_size = len(q_table)

# ============================================
# PRINT RESULTS
# ============================================

print("\n========== TRAINING METRICS ==========")

print(f"Total Games: {total_games}")

print(f"Player 1 Wins: {player1_wins}")
print(f"Player 2 Wins: {player2_wins}")

print(f"Player 1 Win Rate: {player1_rate:.2f}%")
print(f"Player 2 Win Rate: {player2_rate:.2f}%")

print(f"Final Epsilon: {final_epsilon:.4f}")

print(f"Q-table Entries: {qtable_size}")

print("======================================")

# ============================================
# Save report summary
# ============================================

with open("results/final_metrics.txt", "w") as file:

    file.write("TRAINING METRICS\n")
    file.write("====================\n\n")

    file.write(f"Total Games: {total_games}\n")

    file.write(f"Player 1 Wins: {player1_wins}\n")
    file.write(f"Player 2 Wins: {player2_wins}\n\n")

    file.write(f"Player 1 Win Rate: {player1_rate:.2f}%\n")
    file.write(f"Player 2 Win Rate: {player2_rate:.2f}%\n\n")

    file.write(f"Final Epsilon: {final_epsilon:.4f}\n")

    file.write(f"Q-table Entries: {qtable_size}\n")

print("\nSaved final_metrics.txt")