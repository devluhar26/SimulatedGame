# SimulatedGame – High-Frequency Trading Simulator

A professional-grade **high-frequency trading (HFT) simulator** that functions as a fully-fledged exchange, not just a toy market. Built for developers, educators, and traders to test strategies, understand market microstructure, and simulate institutional-grade trading dynamics.

---

## 🚀 Overview

Unlike most market simulators that rely on randomness, **SimulatedGame** uses live order book dynamics and FIX protocol messaging to mirror real market behaviour. Designed with modularity and scalability in mind, the simulator supports multi-agent trading, realistic participant behavior, and robust API access for custom strategies.

Originally developed as a tool for **recruitment**, **strategy testing**, and **financial education**, this platform brings **real-time, multi-user** market simulation to your local machine or a web server.

---

## 🔑 Key Features

- **True Market Mechanics**  
  Price discovery is driven by order flow and liquidity interaction—no random walk models.

- **Simulated Market Participants**  
  Bots act as institutional investors, market makers, and retail traders—each with unique behaviors and timing.

- **FIX Protocol Integration**  
  Supports FIX messaging for orders, execution reports, and more—just like a real-world electronic exchange.

- **Open API for Strategy Deployment**  
  Plug in your own Python strategies or connect external platforms for testing and analytics.

- **Scalable Multiplayer Engine**  
  Web-based interaction allows multiple users to trade in the same environment with shared market impact.

---

## 🧠 Skills & Tech Stack

- **Languages:** Python, SQL  
- **Core Concepts:** HFT, Market Microstructure, Multi-Agent Simulation, Quantitative Finance  
- **Protocols:** FIX Protocol  
- **Engineering:** Real-time Systems, API Design, Simulation Architecture  

---

## ⚙️ Installation

```bash
git clone https://github.com/devluhar26/SimulatedGame.git
cd SimulatedGame

# Install dependencies (recommend using a virtualenv)
pip install -r requirements.txt

# Start the server
python main.py
