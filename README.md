# Morabaraba AI - Nine Men's Morris with Q-Learning

A complete implementation of the Morabaraba (Nine Men's Morris) board game with a PyGame GUI and Q-Learning AI training system.

## Project Structure

- **`environment.py`** - Core game engine (450+ lines)
  - Game state management and rule enforcement
  - RL interface: `get_state()`, `get_actions()`, `rl_step(action)`
  - UI interface: `step(position)` for manual play
  - Complete Morabaraba rules:
    - Placement phase (each player places 12 pieces)
    - Movement phase (pieces move on board edges)
    - Flying rule (3-piece players can move anywhere)
    - Mill formation and capture (can't capture from mills unless forced)
    - Win conditions (opponent has <3 pieces or no legal moves)

- **`agent.py`** - Q-Learning agent (170 lines)
  - Epsilon-greedy action selection
  - Q-value table learning
  - Epsilon decay (0.995 per episode, minimum 0.01)

- **`train.py`** - Self-play training loop (120 lines)
  - 5000 episodes of self-play
  - Automatic data logging to `results/` folder:
    - `training_data.csv` - Episode stats (episode, winner, epsilon)
    - `training_log.txt` - Detailed logs per episode
  - Progress printed every 10 episodes

- **`main.py`** - PyGame GUI (250 lines)
  - Interactive board visualization
  - Click to place/move pieces
  - Automatic capture prompts
  - Game-over detection and display

- **`evaluate.py`** - Game evaluation tools
  - Performance metrics
  - Match statistics

- **`utils.py`** - Helper functions
  - Common utilities

- **`requirements.txt`** - Dependencies
  - pygame==2.6.1
  - numpy
  - Other standard libraries

## Running the Game

### 1. Interactive Play (PyGame GUI)
```bash
python main.py
```
- Click on board positions to place pieces during placement phase
- Click piece to select, then click destination to move during movement phase
- Red and black pieces alternate turns
- Game automatically detects and displays winner

### 2. RL Training
```bash
python train.py
```
- Trains AI for 5000 episodes
- Saves results to `results/training_data.csv` and `results/training_log.txt`
- Progress printed every 10 episodes
- Takes ~10-30 minutes depending on system

### 3. Evaluate Trained Agent
```bash
python evaluate.py
```
- Performance analysis of trained model
- Match statistics and win rates

## Game Rules

### Board Layout
- 24 positions arranged in 3 concentric squares
- 16 possible mills (3 in a row, on edges or diagonals)
- Positions connected by edges (pieces can only move along connections)

### Phases

#### Placement Phase
- Players alternate placing 12 pieces each on empty board positions
- When 3+ pieces are placed and form a mill, opponent must be captured
- Cannot capture from a mill if open pieces exist elsewhere
- Transition to movement phase after all pieces placed

#### Movement Phase
- Players alternate moving pieces to adjacent empty positions
- Normal rule: Pieces with >3 count move on board edges only
- Flying rule: Players with exactly 3 pieces can move to any empty position
- Capture rules same as placement (remove opponent piece)
- Win if opponent has <3 pieces OR has no legal moves

## RL Integration

### State Representation
28-element tuple:
- `board[24]` - Piece positions (1=player1, -1=player2, 0=empty)
- `selected_piece` - Currently selected piece index (-1 if none)
- `current_player` - Whose turn (1 or -1)
- `capture_mode` - In capture phase (0 or 1)
- `phase` - Game phase (0=placement, 1=movement)

### Action Format
- Tuples: `("place", position)`, `("move", position)`, `("capture", position)`, `("select", position)`
- `get_actions()` returns only legal actions for current state

### Reward Structure
- +1 for winning an episode
- -1 for losing
- 0 for neutral transitions
- Bonus for phase transitions (encouraging progression)

## Training Results

After 5000 episodes:
- Epsilon decays from 1.0 to ~0.0037 (min 0.01)
- Win distribution tracked per player
- Episode statistics logged automatically
- Q-table learns game strategy through self-play

## Technical Details

- **Python 3.11.9** with venv
- **PyGame 2.6.1** (SDL 2.28.4)
- **Episode limit:** 500 steps per episode (prevents infinite loops)
- **Q-Learning hyperparameters:**
  - Learning rate (α) = 0.1
  - Discount factor (γ) = 0.9
  - Initial epsilon = 1.0
  - Epsilon decay = 0.995
  - Minimum epsilon = 0.01

## Files Generated During Training

```
results/
├── training_data.csv      # Episode statistics
└── training_log.txt       # Detailed logs
```

## Troubleshooting

**Issue: Episodes timeout at 500 steps**
- Normal for early training (random play has no clear winner)
- Improves as epsilon decreases and strategy develops

**Issue: No moves available**
- Check `get_actions()` for current game state
- Ensure `has_legal_moves()` properly evaluates flying rule

**Issue: PyGame display issues**
- Requires SDL 2.28+ (included with pygame 2.6.1)
- Tested on Windows 10/11

## Development Notes

All game logic is self-contained in `environment.py`. The RL interface (`rl_step()`, `get_state()`, `get_actions()`) is decoupled from the UI interface (`step()`), allowing:
- Training without graphics (faster)
- Manual play through GUI
- Custom agents (just implement `choose_action()`)
- Game evaluation and analysis

See inline code comments for detailed method documentation.
