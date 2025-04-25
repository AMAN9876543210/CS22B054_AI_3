# aman_anand_minimax_game.py

import gym
import slimevolleygym
from slimevolleygym.patch_env import patch_env
from slimevolleygym.slimevolley import SlimeVolleyEnv
from algorithm.minimax import minimax
from algorithm.random_agent import RandomAgent

import numpy as np
import imageio
import cv2
import time

# Patch environment for compatibility (necessary for SlimeVolley)
patch_env()

# Render the game frame with current scores and optional final result
def render_frame_with_score(environment, yellow_score, blue_score, final=False):
    frame = environment.render(mode="rgb_array")
    frame_overlay = frame.copy()
    text_color = (255, 255, 255)

    # Display live scores
    cv2.putText(frame_overlay, f"Yellow: {yellow_score} | Blue: {blue_score}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

    # Display final result if it's the end
    if final:
        if yellow_score > blue_score:
            result = "Yellow Wins!"
        elif blue_score > yellow_score:
            result = "Blue Wins!"
        else:
            result = "It's a Draw!"
        cv2.putText(frame_overlay, result, (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3, cv2.LINE_AA)

    return frame_overlay

# Main function to run the game using Minimax algorithm
def run_minimax_game():
    environment = gym.make("SlimeVolley-v0")
    observation = environment.reset()
    recorded_frames = []
    yellow_score = 0
    blue_score = 0

    fps = 30
    match_duration_seconds = 15
    max_frame_count = fps * match_duration_seconds

    opponent_agent = RandomAgent()
    actual_frame_count = 0
    start_time = time.time()

    for _ in range(max_frame_count):
        frame = render_frame_with_score(environment, yellow_score, blue_score)
        recorded_frames.append(frame)

        # Get the best action from the Minimax agent
        _, best_action = minimax(environment, observation, depth=3, maximizing_player=True)
        if best_action is None:
            best_action = np.array([0, 0, 0])  # fallback to "do nothing"

        opponent_action = opponent_agent.act(observation)

        observation, reward, done, _ = environment.step(best_action, opponent_action)
        actual_frame_count += 1

        if reward == 1:
            yellow_score += 1
        elif reward == -1:
            blue_score += 1

        if done:
            observation = environment.reset()

    end_time = time.time()
    total_runtime = end_time - start_time

    # Add extra frames at end to show the final result
    final_result_frame = render_frame_with_score(environment, yellow_score, blue_score, final=True)
    for _ in range(fps * 2):
        recorded_frames.append(final_result_frame)

    environment.close()

    # Resize video frames to dimensions divisible by 16
    height, width, _ = recorded_frames[0].shape
    height = ((height + 15) // 16) * 16
    width = ((width + 15) // 16) * 16
    resized_frames = [cv2.resize(f, (width, height)) for f in recorded_frames]

    output_video_path = "minimax_fullgame.mp4"
    imageio.mimsave(output_video_path, resized_frames, fps=fps)

    # Show stats
    print(f"✅ Saved full 15-second game to {output_video_path}")
    print("\n📊 Match Stats (Minimax):")
    print(f"Total Score: Yellow {yellow_score} - Blue {blue_score}")
    print(f"Total Frames Played: {actual_frame_count}")
    print(f"Execution Time: {total_runtime:.2f} seconds")

# Start the game when this script is run directly
if __name__ == "__main__":
    run_minimax_game()

# Code by Aman Anand 
