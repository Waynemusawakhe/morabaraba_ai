# ============================================
# train.py
# Self-play training with automatic logging
# ============================================

import os
import csv
import datetime
from environment import MorabarabaEnv
from agent import QLearningAgent

RESULTS_DIR = "results"
TRAINING_CSV = os.path.join(RESULTS_DIR, "training_data.csv")
TRAINING_LOG = os.path.join(RESULTS_DIR, "training_log.txt")
QTABLE_FILE = os.path.join(RESULTS_DIR, "qtable.pkl")

EPISODES = 5000

# create results folder
os.makedirs(RESULTS_DIR, exist_ok=True)

# preserve previous results if they exist
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for path in (TRAINING_CSV, TRAINING_LOG, QTABLE_FILE):
    if os.path.exists(path):
        base, ext = os.path.splitext(path)
        backup_path = f"{base}_{timestamp}{ext}"
        os.rename(path, backup_path)
        print(f"Backed up existing file: {path} -> {backup_path}")

print(f"Starting training for {EPISODES} episodes...")

env = MorabarabaEnv()
agent = QLearningAgent()

# CSV file setup
csv_file = open(TRAINING_CSV, "w", newline="")
csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "episode",
    "winner",
    "epsilon"
])

wins = {1: 0, -1: 0}

log_file = open("results/training_log.txt", "w")

for episode in range(EPISODES):

    state = env.reset()
    done = False

    episode_reward = 0
    steps = 0
    max_steps = 500  # prevent infinite loops

    while not done and steps < max_steps:

        actions = env.get_actions()

        if not actions:
            break

        action = agent.choose_action(state, actions)

        next_state, reward, done = env.rl_step(action)

        next_actions = env.get_actions()

        agent.update_q_value(
            state,
            action,
            reward,
            next_state,
            next_actions
        )

        state = next_state
        episode_reward += reward
        steps += 1

    # record winner
    winner = env.winner

    if winner is not None:
        wins[winner] += 1

    # decay exploration
    agent.decay_epsilon()

    # ================================
    # SAVE DATA AUTOMATICALLY
    # ================================

    csv_writer.writerow([
        episode,
        winner,
        agent.epsilon
    ])

    log_file.write(
        f"Episode {episode} | Winner: {winner} | "
        f"Reward: {episode_reward:.2f} | "
        f"Epsilon: {agent.epsilon:.4f}\n"
    )

    # ================================
    # PROGRESS OUTPUT
    # ================================

    if episode % 10 == 0 or episode == EPISODES - 1:

        print("\nEpisode:", episode)
        print("Wins:", wins)
        print("Epsilon:", agent.epsilon)
        print("--------------------------------")

print("Training complete")
csv_file.close()
log_file.close()

agent.save_q_table()

print("\nTraining complete.")
print("Q-table saved.")