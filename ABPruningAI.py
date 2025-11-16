import copy
from MancalaGame import Mancala

class ABPruningAI:
    def __init__(self, game: Mancala, playing=1, depth=5):
       
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
   
    def minimax_alphabeta(self, state: Mancala, depth, maximizing, alpha, beta):
        """
        Alpha:this will give us our best value maximizer
        Beta: this will give us our best value minimizer
        Prunes branches that can't affect final decision
        returns: this will return our best move
        """
        if depth == 0 or state.winning_eval():
            return self.heuristic(state), None
           
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return self.heuristic(state), None
       
        top_move = None
       
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                next_state = copy.deepcopy(state)
                next_state.play(move)
                eval_score, _ = self.minimax_alphabeta(next_state, depth - 1, False, alpha, beta)
               
                if eval_score > max_eval:
                    max_eval = eval_score
                    top_move = move
               
                # our actual alpha betta prune
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # this is where we cut off what we dont neeed to visit
                   
            return max_eval, top_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                next_state = copy.deepcopy(state)
                next_state.play(move)
                eval_score, _ = self.minimax_alphabeta(next_state, depth - 1, True, alpha, beta)
               
                if eval_score < min_eval:
                    min_eval = eval_score
                    top_move = move
               
               
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  #cutting off the remaining branchess
                   
            return min_eval, top_move
       
    def choose_move(self):
        maximizing = (self.game.current_player == self.playing)

        _, top_move = self.minimax_alphabeta(
            self.game,
            self.max_depth,
            maximizing,
            float('-inf'),  # our first alpha
            float('inf')    # our first beta
        )
        return top_move