# 🏐 SlimeVolley AI Agents: Minimax vs AlphaBeta

This project implements AI agents for the [SlimeVolleyGym](https://github.com/hardmaru/slimevolleygym) environment using classic search algorithms: **Minimax** and **Alpha-Beta Pruning**. The agents play against a random opponent and generate gameplay videos to evaluate performance.

---

## 📁 Project Structure

```
CS22B054_AI_3/                           
├── pycache/                                            # Compiled Python cache
├── algorithm/ │ ├── pycache/                           # Compiled Python cache for algorithm module
│ ├── alphabeta.py                                      # AlphaBeta pruning agent logic
│ ├── eval_utils.py                                     # Evaluation utility functions
│ ├── minimax.py                                        # Minimax agent logic
│ └── random_agent.py                                   # Baseline random agent
├── slimevolleygym/                                     # SlimeVolley environment
├── run_alphabeta.py                                    # Script to run AlphaBeta agent
├── run_minimax.py                                      # Script to run Minimax agent
├── result.py                                           # Script to evaluate and collect results
├── alphabeta_dynamic_fps.mp4                           # Output video for alphabeta agent
├── minimax_dynamic_fps.mp4                             # Output video for minimax agent
├── requirements.txt                                    # Project dependencies
├── LICENSE                                             # License information
└── README.md                                           # Readme file

```
## 🚀 Installation

### 1. Clone the repository
```bash
git clone git@github.com:AMAN9876543210/CS22B054_AI_3.git
cd CS22B054_AI_3
```
### 2. Set up virtual environment

Run the following command to create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## 🎮🤖 AI Agents: Minimax vs AlphaBeta

This project includes AI agents for playing a game using **Minimax** and **AlphaBeta** algorithms. The agents are evaluated by playing the game and generating videos of their performances.

### Watch the AI Agents in Action:

- [Minimax vs RandomAgent](https://github.com/AMAN9876543210/CS22B054_AI_3/blob/main/minimax_dynamic_fps.mp4)
- [AlphaBeta vs RandomAgent](https://github.com/AMAN9876543210/CS22B054_AI_3/blob/main/alphabeta_dynamic_fps.mp4)

Click the above links to view the performance of Minimax and AlphaBeta agents in the game.


## 🧠 Agents

### Minimax
- Explores all possible future actions up to a fixed depth.
- Assumes optimal play from both sides.
- Slower but precise.

### Alpha-Beta Pruning
- Optimized version of Minimax.
- Skips unnecessary branches using pruning.
- Faster with the same result as Minimax (if fully expanded).

### Random Agent
- Acts as a baseline opponent.
- Picks random valid actions.

## 🕹️ Running the Game

To run the game, execute the following command:

```bash
python3  result.py
```
### This script will:
- Run both **Minimax vs RandomAgent** and **AlphaBeta vs RandomAgent**.
- Render and save gameplay videos in `.mp4` format.
- Display scores and timing statistics for each match.

## 🏁 Match Results
Each agent plays for a fixed number of frames (100 steps) and the results are rendered with score overlays and winner declaration.


### 🏁 Running Minimax vs RandomAgent...

#### 📊 Match Stats (Minimax):
- **Final Score**: Yellow 0 - Blue 1  
- **Real-time Duration**: 3.35s  
- **Adjusted FPS**: 22.41 (Base: 29.87, Speed Factor: 0.75x)  
- **Total Frames Saved**: 145  
- **Video Output**: `minimax_dynamic_fps.mp4`

---

### 🏁 Running AlphaBeta vs RandomAgent...

#### 📊 Match Stats (AlphaBeta):
- **Final Score**: Yellow 0 - Blue 3  
- **Real-time Duration**: 1.66s  
- **Adjusted FPS**: 45.05 (Base: 60.07, Speed Factor: 0.75x)  
- **Total Frames Saved**: 190  
- **Video Output**: `alphabeta_dynamic_fps.mp4`

## 🔍 How It Works

### `evaluate_position()`
- Evaluates a state based on how close the player is to the ball.

### `alphabeta()` and `minimax()`
- Use depth-limited search to choose the best action.
- Simulate future game states using the **SlimeVolleyEnv**'s internal state cloning.

### `render_frame_with_score()`
- Overlays scores and winner text on each rendered frame using **OpenCV**.


## 📚 Requirements
```
pyglet==1.5.11
gym==0.21.0
slimevolleygym==0.1.0
numpy==1.23.5
opencv-python==4.9.0.80
imageio==2.34.0
imageio-ffmpeg==0.4.9
```
### Install with:

```bash
pip install -r requirements.txt
```
## 🙋 Author

**Aman Anand**
Roll No: CS22B054

