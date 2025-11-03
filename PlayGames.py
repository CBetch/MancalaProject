from MancalaGame import Mancala
from MinimaxAI import MinimaxAI

class PlayGames:
    def __init__(self, p1type, p2type, numberGames=100, verbose=False):
        """
            Player Types:
                random
                minimax
        """
        self.p1type = p1type
        self.p2type = p2type
        self.numberGames = numberGames
        self.verbose = verbose
        print(f"Playing {self.numberGames} games of {self.p1type} vs {self.p2type}...")

    def play_games(self, max_moves=500):
        '''
        results['status'] tracks win/loss status
                1: player 1 win
                2: player 2 win
                0: tie
        results['score] tracks tuples (p1_score, p2_score)
        results['num_moves] tracks #moves for each game
        '''
        results = {
            'status': [],
            'score': [],
            'num_moves': []
        }
        for game_num in range(1, self.numberGames+1):
            if self.verbose:
                if game_num % 10 == 0:
                    print(f"Playing Game {game_num}/{self.numberGames}...")

            game = Mancala()
            # Play until game is over (default 500 move max to prevent infinite loops)
            move_count = 0
            while not game.winning_eval() and move_count < max_moves:
                # Determine next move depening on p1/p2 type
                move = None
                if game.current_player == 1:
                    if self.p1type == "random":
                        move = game.random_move_generator()
                    elif self.p1type == "minimax":
                        ai = MinimaxAI(game, 1)
                        move = ai.choose_move()
                    else:
                        print("Invalid p1type, using random move")
                        move = game.random_move_generator()
                else:
                    if self.p1type == "random":
                        move = game.random_move_generator()
                    elif self.p1type == "minimax":
                        ai = MinimaxAI(game, 2)
                        move = ai.choose_move()
                    else:
                        print("Invalid p2type, using random move")
                        move = game.random_move_generator()
                # Play the move
                game.play(move)
                move_count += 1
                
            # Add game to results
            p1_score = game.board[game.p1_mancala_index]
            p2_score = game.board[game.p2_mancala_index]
            if p1_score > p2_score:
                results['status'].append(1)
            elif p1_score < p2_score:
                results['status'].append(2)
            else:
                results['status'].append(0)
            results['score'].append((p1_score, p2_score))
            results['num_moves'].append(move_count)
        
        # Return results after all games finish
        return results