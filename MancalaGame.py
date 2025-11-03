import random

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4, verbose = False):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        self.verbose = verbose
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def __str__(self):
        self.display_board()
        return ""

    def display_board(self):
        """
        Print Condensed Board
        """
        p1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        p1_man = self.board[self.p1_mancala_index]
        p2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        p2_man = self.board[self.p2_mancala_index]

        def fn(n):
            return f"{n}" if n >= 10 else f" {n}"

        # P1 Mancala
        lines = [
            " 1", 
            f"{fn(p1_man)}", 
            "<-"
        ]
        # Pits
        mid = f"     Player:  {self.current_player}     " + "   " * (len(p1_pits) - 6)
        for i in range(len(p1_pits)):
            lines = [p + s for p, s in zip(lines, [
                f" {fn(p1_pits[i])}", 
                mid[i*3:(i+1)*3], 
                f" {fn(p2_pits[i])}"
            ])]
        # P2 Mancala
        lines = [p + s for p, s in zip(lines, [
            "  -> ", 
            f" {fn(p2_man)}  ", 
            "  2  "
        ])]
        # Output
        [print(line) for line in lines]
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        # Check pit selection between 1-6 (1-index)
        if pit > 0 and pit <= self.pits_per_player:
            # Make sure there's at least one stone in the pit chosen
                # Side note, why would p1/2_pits_index have two elements rather than containing the indexes of each players pits on the board?
            if self.current_player == 1:
                if self.board[pit-1 + self.p1_pits_index[0]] > 0:
                    return True
            else:
                if self.board[pit-1 + self.p2_pits_index[0]] > 0:
                    return True

        return False
        
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        valid_pits = self.get_valid_moves()
        # Return random valid pit
        return random.choice(valid_pits)

    def get_valid_moves(self):
        """
        Returns an array of valid pits for the current player ([1-i])
        """
        # Get array of valid pits
        valid_pits = []
        adj_i = self.p1_pits_index[0] if self.current_player == 1 else self.p2_pits_index[0] # Adjust board index based on player
        for i in range(0, self.pits_per_player):    # /
            if self.board[i + adj_i] > 0:           # | Add pits with more than 1 stone on current players side to valid choices
                valid_pits.append(i+1)                 # \
        return valid_pits

    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        
        # Make sure the pit chosen is a valid move
        if not self.valid_move(pit):
            if self.verbose:
                print("INVALID MOVE")
            return self.board

        # Verify if the board is in a winning state
        if self.winning_eval():
            if self.verbose:
                print("GAME OVER")
            return self.board
        
        # Take turn
        curr_index = pit-1 + self.p1_pits_index[0] if self.current_player == 1 else pit-1 + self.p2_pits_index[0]   # Track which pit we're looking at
        cur_mancala_idx = self.p1_mancala_index if self.current_player == 1 else self.p2_mancala_index
        opp_mancala_idx = self.p2_mancala_index if self.current_player == 1 else self.p1_mancala_index # Identify the index to skip (opponents mancala)
        stones_in_hand = self.board[curr_index]                                 # /
        self.board[curr_index] = 0                                              # | "Pick up" stones in the current pit, and shift pointer to the next pit
        curr_index = curr_index + 1 if curr_index < len(self.board)-1 else 0    # \

        # Distribute stones
        while stones_in_hand > 1:
            if curr_index != opp_mancala_idx:
                self.board[curr_index] += 1
                stones_in_hand -= 1
            curr_index = curr_index + 1 if curr_index < len(self.board)-1 else 0    # Properly shift curr_index pointer
        # Last stone, special. Claim opposite pit and the stone if it lands in an empty pit on players side
        if curr_index == opp_mancala_idx:
            curr_index = curr_index + 1 if curr_index < len(self.board)-1 else 0
            self.board[curr_index] += 1
        elif curr_index == cur_mancala_idx or self.board[curr_index] != 0:
            self.board[curr_index] += 1
        elif self.current_player == 1 and (curr_index > self.p1_pits_index[1] or curr_index < self.p1_pits_index[0]):
            self.board[curr_index] += 1
        elif self.current_player == 2 and (curr_index > self.p2_pits_index[1] or curr_index < self.p2_pits_index[0]):
            self.board[curr_index] += 1
        else:
            # Capture opposite stones
            p1_pits = [i for i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1)]
            p2_pits = [i for i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1)]
            p2_pits.reverse()
            captured_stones = 0
            # Find pit of opposite side of board, clear, and capture stones
            if curr_index in p1_pits:
                captured_stones = self.board[p2_pits[p1_pits.index(curr_index)]]
                self.board[p2_pits[p1_pits.index(curr_index)]] = 0
            else:
                captured_stones = self.board[p1_pits[p2_pits.index(curr_index)]]
                self.board[p1_pits[p2_pits.index(curr_index)]] = 0
            # Add to current players mancala
            self.board[cur_mancala_idx] += 1 + captured_stones
        stones_in_hand -= 1



        # Log move, switch player, and return
        self.moves.append((self.current_player, pit))
        self.current_player = 1 if self.current_player == 2 else 2
        return self.board                       
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        # Make sure there's at least 1 stone in at least 1 of each players pits
        end_game = False                                  
        if sum(self.board[self.p1_pits_index[0]:self.p1_pits_index[1]+1]) == 0:  
            end_game = True
        if sum(self.board[self.p2_pits_index[0]:self.p2_pits_index[1]+1]) == 0:  
            end_game = True

        # If game is over, determine the winner and print the score
        if end_game:
            # Distribute remaining stones
            p1_sum = 0
            for i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1):
                p1_sum += self.board[i]
                self.board[i] = 0
            self.board[self.p1_mancala_index] += p1_sum
            p2_sum = 0
            for i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1):
                p2_sum += self.board[i]
                self.board[i] = 0
            self.board[self.p2_mancala_index] += p2_sum
            
            # Determine winner, print
            if self.verbose:
                if self.board[self.p1_mancala_index] == self.board[self.p2_mancala_index]:
                    print("TIE")
                elif self.board[self.p1_mancala_index] >= self.board[self.p2_mancala_index]:
                    print("Player 1 WIN")
                else:
                    print("Player 2 WIN")
                print(f"SCORE: P1({self.board[self.p1_mancala_index]} - {self.board[self.p2_mancala_index]})P2")
        
        # Return if the game is over or not
        return end_game