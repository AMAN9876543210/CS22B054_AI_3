# your_algo/eval_utils.py

# Function to evaluate the state of the game based on various factors
def evaluate_game_state(observation, is_game_over, game_info):
    # Calculate score difference between agent and opponent
    agent_score = game_info['agentScore']
    opponent_score = game_info['opponentScore']
    score_difference = (agent_score - opponent_score) * 1000

    # Add bonus for ball's X position (encourages pushing the ball to the right)
    ball_position_x = observation[4]
    score_difference += 100 * (ball_position_x - 0.5)  # Encourage pushing ball right

    # Add bonus/penalty for moving toward the ball
    agent_position_x = observation[0]
    score_difference -= 10 * abs(agent_position_x - ball_position_x)

    # Game Over Bonus/Penalty
    if is_game_over:
        if agent_score > opponent_score:
            score_difference += 10000  # Bonus for winning
        elif agent_score < opponent_score:
            score_difference -= 10000  # Penalty for losing

    return score_difference

# Aman Anand - The author of this code
