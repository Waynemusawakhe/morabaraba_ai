import pygame
import sys
import time

from environment import MorabarabaEnv
from agent import QLearningAgent

# ============================================
# Initialize pygame
# ============================================

pygame.init()

# ============================================
# Window settings
# ============================================

WIDTH = 800
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Morabaraba AI")

# ============================================
# Colors
# ============================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
YELLOW = (255, 255, 0)

# ============================================
# Fonts
# ============================================

font = pygame.font.SysFont(None, 36)

# ============================================
# Create environment and AI
# ============================================

env = MorabarabaEnv()

agent = QLearningAgent()

# AI should not explore during gameplay
agent.epsilon = 0

# ============================================
# Human vs AI setup
# ============================================

HUMAN_PLAYER = 1
AI_PLAYER = -1

# ============================================
# Node positions
# ============================================

positions = [

    (100,100), (400,100), (700,100),
    (700,400), (700,700), (400,700),
    (100,700), (100,400),

    (200,200), (400,200), (600,200),
    (600,400), (600,600), (400,600),
    (200,600), (200,400),

    (300,300), (400,300), (500,300),
    (500,400), (500,500), (400,500),
    (300,500), (300,400)
]

# ============================================
# Board connections
# ============================================

connections = [

    (0,1), (1,2),
    (2,3), (3,4),
    (4,5), (5,6),
    (6,7), (7,0),

    (8,9), (9,10),
    (10,11), (11,12),
    (12,13), (13,14),
    (14,15), (15,8),

    (16,17), (17,18),
    (18,19), (19,20),
    (20,21), (21,22),
    (22,23), (23,16),

    (1,9), (9,17),
    (3,11), (11,19),
    (5,13), (13,21),
    (7,15), (15,23)
]

# ============================================
# Get clicked node
# ============================================

def get_clicked_node(mouse_pos):

    mx, my = mouse_pos

    for i, position in enumerate(positions):

        px, py = position

        distance = ((mx - px)**2 + (my - py)**2)**0.5

        if distance <= 20:
            return i

    return None

# ============================================
# AI MOVE
# ============================================

def ai_move():

    if env.done:
        return

    if env.current_player != AI_PLAYER:
        return

    actions = env.get_actions()

    if len(actions) == 0:
        return

    state = env.get_state()

    action = agent.choose_action(state, actions)

    next_state, reward, done = env.rl_step(action)

    print(f"AI played {action}")

    if done:
        print("AI finished the game.")
    elif env.capture_mode and action[0] == "capture":
        print("AI captured a piece!")
    elif action[0] == "move":
        print("AI moved a piece.")
    elif action[0] == "place":
        print("AI placed a piece.")

# ============================================
# Main loop
# ============================================

running = True

while running:

    screen.fill(WHITE)

    # ========================================
    # AI TURN
    # ========================================

    if (
        not env.done and
        env.current_player == AI_PLAYER
    ):

        pygame.time.delay(400)

        ai_move()

    # ========================================
    # Draw board lines
    # ========================================

    for connection in connections:

        start = positions[connection[0]]
        end = positions[connection[1]]

        pygame.draw.line(screen, BLACK, start, end, 3)

    # ========================================
    # Draw nodes
    # ========================================

    for i, position in enumerate(positions):

        color = BLUE

        if env.selected_piece == i:
            color = YELLOW

        pygame.draw.circle(screen, color, position, 12)

    # ========================================
    # Draw pieces
    # ========================================

    for i, value in enumerate(env.board):

        x, y = positions[i]

        # Human
        if value == HUMAN_PLAYER:

            pygame.draw.circle(screen, BLACK, (x, y), 25)

        # AI
        elif value == AI_PLAYER:

            pygame.draw.circle(screen, RED, (x, y), 25)

    # ========================================
    # Status text
    # ========================================

    if env.done:

        if env.winner == HUMAN_PLAYER:

            status = "Game over: YOU win"

        else:

            status = "Game over: AI wins"

        text = font.render(status, True, GREEN)

    elif env.capture_mode:

        status = "Capture opponent piece!"

        text = font.render(status, True, GREEN)

    else:

        if env.current_player == HUMAN_PLAYER:

            status = "Your turn"

        else:

            status = "AI thinking..."

        text = font.render(status, True, BLACK)

    screen.blit(text, (20, 780))

    # ========================================
    # Event handling
    # ========================================

    for event in pygame.event.get():

        # Quit
        if event.type == pygame.QUIT:

            running = False

        # ====================================
        # HUMAN CLICK
        # ====================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if env.done:
                continue

            if env.current_player != HUMAN_PLAYER:
                continue

            mouse_pos = pygame.mouse.get_pos()

            node = get_clicked_node(mouse_pos)

            if node is not None:

                # ====================================
                # Capture mode
                # ====================================

                if env.capture_mode:

                    success = env.remove_piece(node)

                    if success:

                        print("Captured opponent piece!")

                    else:

                        print("Invalid capture")

                # ====================================
                # Normal play
                # ====================================

                else:

                    success, mill_formed = env.step(node)

                    if success:

                        print(f"You played node {node}")

                        if mill_formed:

                            print("You formed a mill!")

                    else:

                        print("Illegal move")

    pygame.display.update()

pygame.quit()
sys.exit()