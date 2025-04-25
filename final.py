# aman_anand_minimax_alphabeta_game.py

import gym
import slimevolleygym
from slimevolleygym.patch_env import patch_env
from slimevolleygym.slimevolley import SlimeVolleyEnv

from algorithm.minimax import minimax
from algorithm.alphabeta import alphabeta
from algorithm.random_agent import RandomAgent

import numpy as np
import imageio
import cv2
import time

# Ensure SlimeVolley environment is patched and compatible
patch_env()

# Renders the game frame with current scores and optional final result
def render_frame_with_score(env, yellow_score, blue_score, final=False):
    frame = env.render(mode="rgb_array")
    overlay = frame.copy()
    text_color = (255, 255, 255)

    # Scoreboard display
    cv2.putText(overlay, f"Yellow: {yellow_score} | Blue: {blue_score}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

    # Display winner at end
    if final:
        if yellow_score > blue_score:
            result = "Yellow Wins!"
        elif blue_score > yellow_score:
            result = "Blue Wins!"
        else:
            result = "It's a Draw!"
        cv2.putText(overlay, result, (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3, cv2.LINE_AA)

    return overlay

# Core function to run a game using the specified algorithm
def run_game(algorithm="minimax"):
    env = gym.make("SlimeVolley-v0")
    obs = env.reset()
    frames = []
    yellow_score = 0
    blue_score = 0

    opponent = RandomAgent()
    start_time = time.time()
    speed_factor = 0.75  # Playback 25% slower than real-time

    total_steps = 100  # Game duration (steps)
    for _ in range(total_steps):
        # Render frame with live score
        frame = render_frame_with_score(env, yellow_score, blue_score)
        frames.append(frame)

        # Decide action for yellow agent using chosen algorithm
        if algorithm == "minimax":
            _, action_yellow = minimax(env, obs, depth=3, maximizing_player=True)
        elif algorithm == "alphabeta":
            _, action_yellow = alphabeta(env, obs, 3, float('-inf'), float('inf'), True)

        else:
            raise ValueError("Invalid algorithm. Choose 'minimax' or 'alphabeta'.")

        # Default action if decision failed
        action_yellow = action_yellow if action_yellow is not None else np.array([0, 0, 0])
        action_blue = opponent.act(obs)

        # Execute both actions
        obs, reward, done, _ = env.step(np.hstack([action_yellow, action_blue]))

        # Score updates
        if reward == 1:
            yellow_score += 1
        elif reward == -1:
            blue_score += 1

        if done:
            obs = env.reset()

    # Performance measurement
    elapsed_time = time.time() - start_time
    base_fps = total_steps / elapsed_time if elapsed_time > 0 else 30.0
    adjusted_fps = base_fps * speed_factor

    # Append final scoreboard frame
    final_frame = render_frame_with_score(env, yellow_score, blue_score, final=True)
    for _ in range(int(round(2 * adjusted_fps))):
        frames.append(final_frame)

    env.close()

    # Adjust video resolution (divisible by 16)
    h, w, _ = frames[0].shape
    h = ((h + 15) // 16) * 16
    w = ((w + 15) // 16) * 16

    output_file = f"{algorithm}_dynamic_fps.mp4"
    with imageio.get_writer(output_file, fps=adjusted_fps) as writer:
        for frame in frames:
            resized = cv2.resize(frame, (w, h))
            writer.append_data(resized)

    # Stats output
    print(f"\n📊 Match Stats ({algorithm.capitalize()}):")
    print(f"Final Score: Yellow {yellow_score} - Blue {blue_score}")
    print(f"Real-time Duration: {elapsed_time:.2f}s")
    print(f"Adjusted FPS: {adjusted_fps:.2f} (Base: {base_fps:.2f}, Speed Factor: {speed_factor}x)")
    print(f"Total Frames Saved: {len(frames)}")
    print(f"Video Output: {output_file}")

# Run both agents in sequence
def run_both_algorithms():
    print("🏁 Running Minimax vs RandomAgent...")
    run_game(algorithm="minimax")

    print("\n🏁 Running AlphaBeta vs RandomAgent...")
    run_game(algorithm="alphabeta")

# Script entry point
if __name__ == "__main__":
    run_both_algorithms()

# coded by Aman Anand 
