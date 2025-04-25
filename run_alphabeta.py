# aman_anand_alphabeta_game.py

import gym
import time
import slimevolleygym
from slimevolleygym.patch_env import patch_env
from slimevolleygym.slimevolley import SlimeVolleyEnv
from algorithm.alphabeta import alphabeta
from algorithm.random_agent import RandomAgent

import numpy as np
import imageio
import cv2

# Ensure compatibility with the environment
patch_env()

# Render frame with current score and optionally a final winner message
def render_frame_with_score(environment, yellow_score, blue_score, final=False):
    frame = environment.render(mode="rgb_array")
    frame_copy = frame.copy()
    text_color = (255, 255, 255)

    cv2.putText(frame_copy, f"Yellow: {yellow_score} | Blue: {blue_score}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

    if final:
        if yellow_score > blue_score:
            winner_text = "Yellow Wins!"
        elif blue_score > yellow_score:
            winner_text = "Blue Wins!"
        else:
            winner_text = "It's a Draw!"
        cv2.putText(frame_copy, winner_text, (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3, cv2.LINE_AA)

    return frame_copy

# Run a full AlphaBeta vs RandomAgent game and save to video
def run_alphabeta_game():
    environment = gym.make("SlimeVolley-v0")
    observation = environment.reset()
    recorded_frames = []
    yellow_score = 0
    blue_score = 0

    frames_per_second = 30
    match_duration_seconds = 15
    max_frame_count = frames_per_second * match_duration_seconds

    opponent_agent = RandomAgent()

    start_timer = time.time()

    for step in range(max_frame_count):
        frame = render_frame_with_score(environment, yellow_score, blue_score)
        recorded_frames.append(frame)

        # Use AlphaBeta to select the best action
        _, best_action = alphabeta(
            environment,
            observation,
            depth=3,
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=True
        )

        # Default to "do nothing" if action is None
        if best_action is None:
            best_action = np.array([0, 0, 0])

        random_action = opponent_agent.act(observation)

        # Step through the environment with both actions
        observation, reward, done, _ = environment.step(best_action, random_action)

        # Update scores
        if reward == 1:
            yellow_score += 1
        elif reward == -1:
            blue_score += 1

        # Restart game if match ends
        if done:
            observation = environment.reset()

    # Add a few final frames to show the result at the end
    ending_frame = render_frame_with_score(environment, yellow_score, blue_score, final=True)
    for _ in range(frames_per_second * 2):
        recorded_frames.append(ending_frame)

    environment.close()

    # Resize for video consistency
    frame_height, frame_width, _ = recorded_frames[0].shape
    frame_height = ((frame_height + 15) // 16) * 16
    frame_width = ((frame_width + 15) // 16) * 16
    resized_frames = [cv2.resize(f, (frame_width, frame_height)) for f in recorded_frames]

    output_file = "alphabeta_fullgame.mp4"
    imageio.mimsave(output_file, resized_frames, fps=frames_per_second)

    total_time = time.time() - start_timer
    print(f"✅ Saved 15-second AlphaBeta game to {output_file}")
    print(f"Total frames recorded: {len(recorded_frames)}")
    print(f"Execution time: {total_time:.2f} seconds")
    print(f"Final Score — Yellow: {yellow_score}, Blue: {blue_score}")

# Run the game if script is executed directly
if __name__ == "__main__":
    run_alphabeta_game()

# Code by Aman Anand 
