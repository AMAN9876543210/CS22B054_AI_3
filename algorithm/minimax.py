# slimevolleygym/algorithm/minimax.py

import numpy as np

# Define the possible actions for the agent
ACTION_SPACE = [
    np.array([0, 0, 0]),  # Do nothing
    np.array([1, 0, 0]),  # Move left
    np.array([0, 1, 0]),  # Jump
    np.array([0, 0, 1]),  # Move right
    np.array([1, 1, 0]),  # Move left + jump
    np.array([0, 1, 1]),  # Move right + jump
    np.array([1, 0, 1]),  # Move left + right (invalid, but harmless)
]

# Evaluation function to estimate the "goodness" of a game state
def evaluate_game_state(observation):
    # Reward the agent for being closer to the ball
    ball_position_x = observation[4]
    agent_position_x = observation[0]
    return -abs(ball_position_x - agent_position_x)  # Closer to the ball is better

# Minimax algorithm to recursively select the best move
def minimax(env, observation, depth, maximizing_player):
    if depth == 0:
        return evaluate_game_state(observation), None

    # Set initial best value based on whether we are maximizing or minimizing
    best_value = float("-inf") if maximizing_player else float("inf")
    best_action = None

    # Explore all possible actions
    for action in ACTION_SPACE:
        state = env.clone_state()  # Save current game state
        action_opponent = np.array([0, 0, 0])  # Assume opponent does nothing

        # Apply the action for the current player (maximizing or minimizing)
        joint_action = np.hstack([action, action_opponent])
        new_observation, reward, done, info = env.step(joint_action)

        # Recursively evaluate the new game state
        value, _ = minimax(env, new_observation, depth - 1, not maximizing_player)
        env.restore_state(state)  # Restore the game state after the simulation

        # Update the best value and action based on the evaluation
        if maximizing_player and value > best_value:
            best_value = value
            best_action = action
        elif not maximizing_player and value < best_value:
            best_value = value
            best_action = action

    return best_value, best_action

# Aman Anand - The author of this code
