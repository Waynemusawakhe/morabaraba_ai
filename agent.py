# ============================================
# agent.py
# Q-Learning Agent with Save/Load Support
# ============================================

import random
import pickle
import os


class QLearningAgent:

    def __init__(self):

        # ====================================
        # Q-table
        # ====================================

        self.q_table = {}

        # ====================================
        # Learning parameters
        # ====================================

        self.learning_rate = 0.1
        self.discount_factor = 0.9

        # ====================================
        # Exploration parameters
        # ====================================

        self.epsilon = 1.0
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995

        # ====================================
        # Load previous learning if available
        # ====================================

        self.load_q_table()

    # ========================================
    # Convert board state to tuple
    # ========================================

    def get_state_key(self, state):

        return tuple(state)

    # ========================================
    # Get Q-value
    # ========================================

    def get_q_value(self, state, action):

        key = (self.get_state_key(state), action)

        if key not in self.q_table:
            self.q_table[key] = 0.0

        return self.q_table[key]

    # ========================================
    # Choose action
    # ========================================

    def choose_action(self, state, actions):

        # Exploration
        if random.uniform(0, 1) < self.epsilon:

            return random.choice(actions)

        # Exploitation
        q_values = []

        for action in actions:

            q = self.get_q_value(state, action)

            q_values.append(q)

        max_q = max(q_values)

        best_actions = []

        for action in actions:

            if self.get_q_value(state, action) == max_q:

                best_actions.append(action)

        return random.choice(best_actions)

    # ========================================
    # Update Q-table
    # ========================================

    def update_q_value(
        self,
        state,
        action,
        reward,
        next_state,
        next_actions
    ):

        current_q = self.get_q_value(state, action)

        # Future Q-value
        if len(next_actions) > 0:

            max_future_q = max(

                [
                    self.get_q_value(next_state, a)
                    for a in next_actions
                ]

            )

        else:

            max_future_q = 0

        # ====================================
        # Q-learning equation
        # ====================================

        new_q = current_q + self.learning_rate * (

            reward +
            self.discount_factor * max_future_q -
            current_q

        )

        key = (self.get_state_key(state), action)

        self.q_table[key] = new_q

    # ========================================
    # Reduce exploration over time
    # ========================================

    def decay_epsilon(self):

        if self.epsilon > self.min_epsilon:

            self.epsilon *= self.epsilon_decay

            if self.epsilon < self.min_epsilon:
                self.epsilon = self.min_epsilon

    # ========================================
    # Save Q-table
    # ========================================

    def save_q_table(self):

        os.makedirs("results", exist_ok=True)

        with open("results/qtable.pkl", "wb") as file:

            pickle.dump(self.q_table, file)

    # ========================================
    # Load Q-table
    # ========================================

    def load_q_table(self):

        if os.path.exists("results/qtable.pkl"):

            with open("results/qtable.pkl", "rb") as file:

                self.q_table = pickle.load(file)

            print("Loaded existing Q-table.")

        else:

            print("No previous Q-table found.")