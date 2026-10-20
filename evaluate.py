# ============================================
# evaluate.py
# Evaluate the trained Q-learning agent against a random opponent
#
# Usage:
#   python evaluate.py                    # 100 games, seed 42
#   python evaluate.py --games 200 --seed 2026
#   python evaluate.py --watch            # watch one game in the terminal
# ============================================

import argparse
import csv
import os
import random
import time

from environment import MorabarabaEnv
from agent import QLearningAgent

RESULTS_DIR = "results"
MAX_STEPS = 500  # same cap as training; a game that reaches it counts as a draw


def play_game(env, agent, agent_side, rng, watch=False):
    """Play one game. agent_side is 1 or -1. Returns (result, steps)."""
    state = env.reset()
    steps = 0

    while not env.done and steps < MAX_STEPS:
        actions = env.get_actions()
        if not actions:
            break

        if env.current_player == agent_side:
            action = agent.choose_action(state, actions)
        else:
            action = rng.choice(actions)

        state, _, _ = env.rl_step(action)
        steps += 1

        if watch:
            print(f"\nMove {steps} | Player {env.current_player} | Action {action}")
            print(env.board)
            time.sleep(0.3)

    if env.winner is None:
        return "draw", steps
    return ("win" if env.winner == agent_side else "loss"), steps


def main():
    parser = argparse.ArgumentParser(description="Evaluate the Morabaraba agent against a random opponent.")
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--watch", action="store_true", help="watch a single game")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    random.seed(args.seed)

    env = MorabarabaEnv()
    agent = QLearningAgent()
    agent.load_q_table()
    agent.epsilon = 0  # greedy play during evaluation

    if args.watch:
        result, steps = play_game(env, agent, 1, rng, watch=True)
        print(f"\nResult for the agent: {result} after {steps} moves")
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = []
    totals = {"win": 0, "loss": 0, "draw": 0}

    for game in range(args.games):
        side = 1 if game % 2 == 0 else -1  # alternate who moves first
        result, steps = play_game(env, agent, side, rng)
        totals[result] += 1
        rows.append([game, side, result, steps])

    with open(os.path.join(RESULTS_DIR, "evaluation_results.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["game", "agent_side", "result", "steps"])
        writer.writerows(rows)

    n = args.games
    summary = (
        f"Evaluation vs random opponent ({n} games, seed {args.seed})\n"
        f"Wins:   {totals['win']} ({totals['win'] / n:.1%})\n"
        f"Losses: {totals['loss']} ({totals['loss'] / n:.1%})\n"
        f"Draws (hit {MAX_STEPS}-step cap): {totals['draw']} ({totals['draw'] / n:.1%})\n"
    )
    with open(os.path.join(RESULTS_DIR, "evaluation_summary.txt"), "w") as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
