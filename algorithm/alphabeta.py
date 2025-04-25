import numpy as np

# Defining possible actions the player can take in the game
AVAILABLE_ACTIONS = [
    np.array([0, 0, 0]), np.array([1, 0, 0]),
    np.array([0, 1, 0]), np.array([0, 0, 1]),
    np.array([1, 1, 0]), np.array([0, 1, 1]),
    np.array([1, 0, 1])
]

# Evaluation function to calculate how good a position is
# This checks how close the ball is to the player
def evaluate_position(observation):
    ball_x = observation[4]  # X position of the ball
    player_x = observation[0]  # X position of the player
    return -abs(ball_x - player_x)  # Return a negative value based on how far the player is from the ball

# The Alpha-Beta pruning algorithm that decides the best action to take
def alphabeta(environment, observation, depth_limit, alpha_value, beta_value, is_maximizing_player):
    # Base case: if depth limit reached, evaluate the position
    if depth_limit == 0:
        return evaluate_position(observation), None

    best_score = float("-inf") if is_maximizing_player else float("inf")
    best_move = None

    # Iterating over all possible actions
    for action in AVAILABLE_ACTIONS:
        # Save the current game state to restore after this move
        current_state = environment.clone_state()
        
        # Assuming the opponent does nothing (for simplicity in this example)
        opponent_action = np.array([0, 0, 0])

        # Forming a joint action by combining the player's and opponent's actions
        combined_action = np.hstack([action, opponent_action])

        # Apply the action in the environment and get the new state
        new_observation, reward, done, info = environment.step(combined_action)

        # Recursively call alpha-beta pruning for the next depth level
        score, _ = alphabeta(environment, new_observation, depth_limit - 1, alpha_value, beta_value, not is_maximizing_player)

        # Restore the previous state of the environment
        environment.restore_state(current_state)

        # Maximizing player chooses the best score (maximizing the score)
        if is_maximizing_player:
            if score > best_score:
                best_score = score
                best_move = action
            alpha_value = max(alpha_value, best_score)
        # Minimizing player chooses the worst score (minimizing the score)
        else:
            if score < best_score:
                best_score = score
                best_move = action
            beta_value = min(beta_value, best_score)

        # Alpha-Beta pruning: if we have found a worse move, stop exploring further
        if beta_value <= alpha_value:
            break

    # Return the best score and the corresponding best move
    return best_score, best_move

# Aman Anand - The author of this code
