import copy
from MancalaGame import Mancala

class MinimaxAI:
    def __init__(self, game: Mancala, playing=1, depth=5):
        """
        Establishes branch recursion depth, and which player the AI is playing as
        """
        self.game = game
        self.max_depth = depth
        self.playing = playing
    
    def heuristic(self, state: Mancala):
        """
        Maximizes differences between own mancala and opponents mancala
        """
        if self.playing == 1:
            return state.board[state.p1_mancala_index] - state.board[state.p2_mancala_index]
        return state.board[state.p2_mancala_index] - state.board[state.p1_mancala_index]
    
    def minimax(self, state: Mancala, depth, maximizing):
        """
        Recursive minimax implementation
        reutrns: heuristic_value, best_move
        """
        if depth == 0 or state.winning_eval():
            return self.heuristic(state), None

        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return self.heuristic(state), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                next_state = copy.deepcopy(state)
                next_state.play(move)
                eval_score, _ = self.minimax(next_state, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                next_state = copy.deepcopy(state)
                next_state.play(move)
                eval_score, _ = self.minimax(next_state, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move
        
    def choose_move(self):
        maximizing = (self.game.current_player == self.playing)
        _, best_move = self.minimax(self.game, self.max_depth, maximizing)
        return best_move