# 🏆 Duo-Othello AI Agent - CSCI-561 Spring 2024

## 📌 Overview
This project is part of **CSCI-561 - Foundations of Artificial Intelligence** at USC. It involves implementing an AI agent to play **Duo-Othello**, a variation of the classic **Reversi/Othello** game. The agent competes against other agents using **game-tree search techniques** like Minimax and Alpha-Beta pruning.

## 🎯 Project Goals
- ✅ Implement a **Duo-Othello AI agent**.
- ✅ Compete against **TA-provided agents** and other students' agents.
- ✅ Optimize **decision-making under time constraints**.
- ✅ Develop an **evaluation function** for strategic gameplay.

## 🕹️ Game Rules
Duo-Othello is similar to Reversi but with some twists:
1. **Board Size**: 🟦 12x12 instead of the standard 8x8.
2. **Starting Pieces**: 🔵 8 pieces in a fixed configuration.
3. **Scoring System**:
   - The player with the most pieces wins.
   - The **second player** (Black 'X') gets a **+1 bonus**.
   - If tied, the player with more remaining **time wins**.

For detailed rules, check out [Reversi on Wikipedia](https://en.wikipedia.org/wiki/Reversi).

## 🛠️ Implementation Details

This AI agent is designed to compete in strategic games using advanced search techniques and heuristic evaluations.

### 🧠 Algorithms Used
- **Minimax Algorithm 🤖** - A decision rule for minimizing the possible loss for a worst-case scenario.
- **Alpha-Beta Pruning ✂️** - An optimization technique to reduce the number of nodes evaluated in Minimax.
- **Heuristic Evaluation Function 🎯** - A custom scoring function to estimate the desirability of game states.


## 🚀 Getting Started
### Prerequisites
- Python 3.x
- Required libraries: `numpy`, `random`, `time`


### ⏳ Time Management
- The AI operates under a **300-second total time limit**.
- It **dynamically adjusts search depth** based on remaining time to ensure efficient gameplay.

## 📌 Future Improvements
- 🌲 Implement **Monte Carlo Tree Search (MCTS)** for probabilistic decision-making.
- 📊 Optimize **heuristic evaluation function** for improved performance.
- 🚀 Add **parallel processing** to enable deeper search within time constraints.
