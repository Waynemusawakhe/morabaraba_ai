# ============================================
# evaluate.py
# Watch trained AI play
# ============================================

import time
from environment import MorabarabaEnv
from agent import QLearningAgent

env = MorabarabaEnv()
agent = QLearningAgent()

# ============================================
# Turn OFF exploration
# ============================================

agent.epsilon = 0

# ============================================
# Run one evaluation game
# ============================================

state = env.reset()

done = False

move_count = 0
max_moves = 200

while not done and move_count < max_moves:

    actions = env.get_actions()

    if len(actions) == 0:
        break

    action = agent.choose_action(state, actions)

    next_state, reward, done = env.rl_step(action)

    state = next_state

    move_count += 1

    # ========================================
    # PRINT BOARD
    # ========================================

    print("\nMove:", move_count)
    print("Player:", env.current_player)
    print(env.board)

    time.sleep(0.5)

# ============================================
# RESULT
# ============================================

print("\nGame Finished")

if move_count >= max_moves:
    print("Max move count reached, terminating evaluation.")

if env.winner is not None:

    print("Winner:", env.winner)

else:

    print("No winner")