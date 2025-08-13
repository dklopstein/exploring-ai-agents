# Game-Playing and Problem-Solving AI Agents

This repository presents a collection of AI algorithms and decision-making frameworks applied across a diverse set of environments, ranging from deterministic pathfinding to stochastic game-play and probabilistic reasoning.  
The project integrates classical search algorithms, reinforcement learning methods, Monte Carlo Tree Search, and constraint satisfaction, demonstrating a broad spectrum of AI capabilities under a unified experimental framework.

---

## Overview

The core objective of this project is to investigate and implement **intelligent agents** capable of operating in both fully observable and partially stochastic environments.  
Through systematic experimentation, each module explores a distinct branch of AI research:

- **Graph Search & Heuristic Pathfinding** – navigating complex terrains with heterogeneous movement costs.
- **Game Tree Search** – reasoning under uncertainty via the *Expectimax* algorithm.
- **Reinforcement Learning** – policy evaluation and control using Monte Carlo, Temporal-Difference, and Q-Learning methods.
- **Monte Carlo Tree Search (MCTS)** – scalable decision-making in combinatorial games such as Gomoku.
- **Constraint Satisfaction** – efficient backtracking for solving high-complexity puzzles like Sudoku.

---

## Modules

### 1. Pathfinding in Weighted Grids
Implements:
- **Depth-First Search (DFS)** – bug-fixed from an intentionally faulty baseline.
- **Breadth-First Search (BFS)** – uniform step-cost exploration.
- **Uniform Cost Search (UCS)** – cost-aware shortest path.
- **A\*** – guided search using Manhattan Distance heuristic.

**Key Insight:** Evaluates trade-offs between uninformed and informed search in environments with impassable and high-cost terrain.

---

### 2. Expectimax for 2048
Models the **AI player** as a max agent and the **computer** as a stochastic chance agent.  
Implements:
- Depth-3 Expectimax search tree
- State evaluation using in-game scoring functions
- Optimal move selection under probabilistic tile generation

**Outcome:** Achieves consistent performance with frequent 512+ tiles and scores exceeding 5,000.

---

### 3. Reinforcement Learning for Blackjack
Discount factor: `γ = 0.95`  
Rewards: `+1` for win, `-1` for loss

Implements:
- **Monte Carlo Policy Evaluation**
- **Temporal-Difference Policy Evaluation**
- **Q-Learning** with ε-greedy exploration (ε = 0.4)

**Key Focus:** Evaluates fixed policies and learns optimal action-value functions for adaptive decision-making.

---

### 4. Monte Carlo Tree Search for Gomoku
Implements:
- Node selection via UCT (Upper Confidence Bound for Trees)
- Rollout simulation to estimate win rates
- Action ranking based on empirical win probabilities

**Result:** With increased simulation budgets (>6000), the AI exhibits competitive strategic play against human opponents.

---

### 5. Constraint Satisfaction for Sudoku
Implements a **backtracking search solver** with optional heuristics:
- Minimum Remaining Values (MRV) – selecting variables with smallest domain first

**Observation:** Heuristics significantly reduce branching factor, enabling faster puzzle resolution.

---

## Research Relevance
While each environment is distinct, they collectively form a **multi-domain AI testbed** for:
- Comparing algorithmic efficiency
- Analyzing decision-making under uncertainty
- Balancing exploration vs. exploitation in dynamic environments
- Understanding the impact of heuristics in search performance

The combined work reflects a progression from **deterministic search** to **probabilistic planning** and **constraint optimization**, mirroring challenges faced in modern AI research.

---

## Usage
Each module is self-contained with its own `ai.py` implementation and usage instructions. Run `python main.py` in each of the separate folders to "play" each game and the UI will tell you how to utilize the AI.

---

## Future Extensions
- Generalized agent interface for cross-domain benchmarking
- Parallelized Monte Carlo simulations for larger decision spaces
- Integration of deep learning function approximators for complex state evaluation

---

**Author:** Derek Klopstein  
**License:** For educational and research purposes only.
