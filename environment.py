# ============================================
# environment.py
# Morabaraba Environment (Clean + RL Ready)
# ============================================

class MorabarabaEnv:

    def __init__(self):

        # ====================================
        # Mill combinations
        # ====================================

        self.mills = [
            (0,1,2), (2,3,4), (4,5,6), (6,7,0),
            (8,9,10), (10,11,12), (12,13,14), (14,15,8),
            (16,17,18), (18,19,20), (20,21,22), (22,23,16),
            (1,9,17), (3,11,19), (5,13,21), (7,15,23)
        ]

        # ====================================
        # Movement graph
        # ====================================

        self.connections = {
            0:[1,7], 1:[0,2,9], 2:[1,3],
            3:[2,4,11], 4:[3,5], 5:[4,6,13],
            6:[5,7], 7:[0,6,15],

            8:[9,15], 9:[1,8,10,17], 10:[9,11],
            11:[3,10,12,19], 12:[11,13], 13:[5,12,14,21],
            14:[13,15], 15:[7,8,14,23],

            16:[17,23], 17:[9,16,18], 18:[17,19],
            19:[11,18,20], 20:[19,21], 21:[13,20,22],
            22:[21,23], 23:[15,16,22]
        }

        self.reset()

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.board = [0] * 24

        self.PLAYER_ONE = 1
        self.PLAYER_TWO = -1

        self.current_player = self.PLAYER_ONE

        self.done = False
        self.winner = None

        self.capture_mode = False
        self.phase = "placement"

        self.player_one_pieces_placed = 0
        self.player_two_pieces_placed = 0

        self.selected_piece = None

        return self.get_state()

    # ========================================
    # BASIC HELPERS
    # ========================================

    def count_player_pieces(self, player):
        return self.board.count(player)

    def get_state(self):
        return tuple(
            self.board +
            [
                -1 if self.selected_piece is None else self.selected_piece,
                self.current_player,
                1 if self.capture_mode else 0,
                1 if self.phase == "movement" else 0
            ]
        )

    # ========================================
    # MILL CHECK
    # ========================================

    def check_mill(self, position):

        player = self.board[position]

        for a, b, c in self.mills:
            if position in (a, b, c):
                if self.board[a] == player and self.board[b] == player and self.board[c] == player:
                    return True

        return False

    # ========================================
    # MILL MEMBERSHIP (for capture rule)
    # ========================================

    def is_part_of_mill(self, position):

        player = self.board[position]
        if player == 0:
            return False

        for a, b, c in self.mills:
            if position in (a, b, c):
                if self.board[a] == player and self.board[b] == player and self.board[c] == player:
                    return True

        return False

    # ========================================
    # LEGAL MOVES CHECK
    # ========================================

    def has_legal_moves(self, player):

        # Flying rule
        if self.phase == "movement" and self.count_player_pieces(player) == 3:
            return any(v == 0 for v in self.board)

        for i, v in enumerate(self.board):
            if v == player:
                for n in self.connections[i]:
                    if self.board[n] == 0:
                        return True

        return False

    # ========================================
    # WINNER CHECK (FIXED)
    # ========================================

    def check_winner(self):

        # Only determine a winner once the game is in the movement phase.
        # During placement, a player may temporarily have fewer than 3 pieces
        # but the game must continue until movement begins.
        if self.phase == "placement":
            return

        p1 = self.count_player_pieces(1)
        p2 = self.count_player_pieces(-1)

        if p1 < 3:
            self.done = True
            self.winner = -1
            return

        if p2 < 3:
            self.done = True
            self.winner = 1
            return

        if not self.has_legal_moves(1):
            self.done = True
            self.winner = -1
            return

        if not self.has_legal_moves(-1):
            self.done = True
            self.winner = 1
            return

    # ========================================
    # REMOVE PIECE
    # ========================================

    def remove_piece(self, position):

        opponent = self.current_player * -1

        if self.board[position] != opponent:
            return False

        # cannot remove mill piece if other pieces exist
        has_open = any(
            self.board[i] == opponent and not self.is_part_of_mill(i)
            for i in range(24)
        )

        if has_open and self.is_part_of_mill(position):
            return False

        self.board[position] = 0
        self.capture_mode = False

        self.check_winner()

        if not self.done:
            self.current_player *= -1

        return True

    # ========================================
    # PLACE PIECE
    # ========================================

    def place_piece(self, position):

        if self.board[position] != 0:
            return False, False

        if self.current_player == 1 and self.player_one_pieces_placed >= 12:
            return False, False

        if self.current_player == -1 and self.player_two_pieces_placed >= 12:
            return False, False

        self.board[position] = self.current_player

        if self.current_player == 1:
            self.player_one_pieces_placed += 1
        else:
            self.player_two_pieces_placed += 1

        formed_mill = self.check_mill(position)

        if self.player_one_pieces_placed >= 12 and self.player_two_pieces_placed >= 12:
            self.phase = "movement"

        if formed_mill:
            self.capture_mode = True
        else:
            self.current_player *= -1

        return True, formed_mill

    # ========================================
    # SELECT PIECE
    # ========================================

    def select_piece(self, position):

        if self.board[position] == self.current_player:
            self.selected_piece = position
            return True

        return False

    # ========================================
    # CAN FLY
    # ========================================

    def can_fly(self, player):
        return self.phase == "movement" and self.count_player_pieces(player) == 3

    # ========================================
    # MOVE PIECE
    # ========================================

    def move_piece(self, destination):

        if self.selected_piece is None:
            return False, False

        if self.board[destination] != 0:
            return False, False

        if not self.can_fly(self.current_player):
            if destination not in self.connections[self.selected_piece]:
                return False, False

        self.board[destination] = self.current_player
        self.board[self.selected_piece] = 0
        self.selected_piece = None

        formed_mill = self.check_mill(destination)

        self.check_winner()

        if formed_mill:
            self.capture_mode = True
        elif not self.done:
            self.current_player *= -1

        return True, formed_mill

    # ========================================
    # RL action interface
    # ========================================

    def get_actions(self):
        if self.done:
            return []

        if self.capture_mode:
            opponent = self.current_player * -1
            open_pieces = [
                i for i, v in enumerate(self.board)
                if v == opponent and not self.is_part_of_mill(i)
            ]

            if open_pieces:
                return [("capture", i) for i in open_pieces]

            return [("capture", i) for i, v in enumerate(self.board) if v == opponent]

        if self.phase == "placement":
            return [("place", i) for i, v in enumerate(self.board) if v == 0]

        actions = []
        for i, v in enumerate(self.board):
            if v == self.current_player:
                actions.append(("select", i))

        if self.selected_piece is not None:
            if self.can_fly(self.current_player):
                destinations = [i for i, v in enumerate(self.board) if v == 0]
            else:
                destinations = [
                    i for i in self.connections[self.selected_piece]
                    if self.board[i] == 0
                ]

            actions += [("move", i) for i in destinations]

        return actions

    def rl_step(self, action):
        state = self.get_state()

        if self.done:
            return state, 0.0, True

        if not isinstance(action, tuple) or len(action) != 2:
            return state, -1.0, False

        action_type, position = action

        if action_type == "capture":
            success = self.remove_piece(position)
            if not success:
                return self.get_state(), -1.0, False

            reward = 10.0 if self.done else 1.0
            return self.get_state(), reward, self.done

        if action_type == "place":
            success, formed_mill = self.place_piece(position)
            if not success:
                return self.get_state(), -1.0, False

            reward = 2.0 if formed_mill else 0.5
            
            # Auto-transition to movement when placement is complete
            if self.phase == "movement":
                reward += 5.0
            
            if self.done:
                reward += 10.0
            return self.get_state(), reward, self.done

        if action_type == "select":
            success = self.select_piece(position)
            if not success:
                return self.get_state(), -1.0, False

            return self.get_state(), 0.0, self.done

        if action_type == "move":
            success, formed_mill = self.move_piece(position)
            if not success:
                return self.get_state(), -1.0, False

            reward = 2.0 if formed_mill else 1.0
            if self.done:
                reward += 10.0
            return self.get_state(), reward, self.done

        return self.get_state(), -1.0, False

    # ========================================
    # STEP (UI ENTRY POINT)
    # ========================================

    def step(self, position):

        if self.done:
            return False, False

        if self.capture_mode:
            return self.remove_piece(position), False

        if self.phase == "placement":
            return self.place_piece(position)

        if self.phase == "movement":

            if self.selected_piece is None:
                return self.select_piece(position), False

            if self.board[position] == self.current_player:
                self.selected_piece = position
                return True, False

            return self.move_piece(position)

        return False, False