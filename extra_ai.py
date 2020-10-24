import game as g
import copy

# I am choosing to implement alpha beta pruning given the fact that this game is a fully
# deterministic game unlike a game like chess where more heuristics have to be used.

class AI:
    """
    This is ai is based off of alpha beta pruning which runs through each possible
    move and propagates back up the score. Certain branchs of the recursive tree
    will be cut off because a maximum score currently exists for the AI. This
    is the move the ai will choose to play.
    """

    def __init__(self, game, player):
        """
        This initializes the AI to be able to run alpha beta pruning
        :param game: the game that is being played
        :param player: the player that the current ai is
        """

        self.game = game
        self.player = player
        self.made_moves = []

    def copy_game(self, game):
        """
        This will deep copy the game so the game will not be changed by running
        through the alpha beta pruning which has to make moves
        :param game:
        :return: the copied game
        """
        game_cp = g.Game()
        game_cp.last_moved_i = game.last_moved_i
        game_cp.last_moved_j = game.last_moved_j
        # make sure board is not connected to the original board
        game_cp.board = copy.deepcopy(game.board)
        return game_cp

    def move_legal(self, game, row, col):
        """
        This will check if the move is legal
        :param game:
        :param row:
        :param col:
        :return:
        """
        game_cp = self.copy_game(game)
        if self.is_terminal(game):
            return False
        try:
            game_cp.make_move(col)
            game_cp.last_moved_i = row
            game_cp.last_moved_j = col
            return True
        except:
            return False

    def get_successors(self, game):
        pos_moves = []
        if not self.is_terminal(game):
            # get columns with pieces already placed
            for col in range(game.COLUMN_NUM):
                #game_cp = self.game()
                #print(game.board)
                for row in range(game.ROW_NUM):
                    # change to not adding nodes after win
                    if row+1 < 6 and game.board[row][col] == None and game.board[row+1][col] != None:
                        #print(self.check_move(game, row, col))
                        if self.move_legal(game, row, col):
                            pos_moves.append((row, col))
                            break
                    if row == game.ROW_NUM - 1:
                        pos_moves.append((row,col))
        return pos_moves

    def is_terminal(self, game):
        res = game.get_winner()
        #print("current w in term: ", res)
        if res != None:
            return True
        return False

    def next_player(self, player):
        if player:
            return player-1
        else:
            return player+1

    def get_score(self, game):
        winner = game.get_winner()
        # print("cur winner: ", winner)
        # print(game.board)
        if winner == self.player:
            return 1
        elif winner == 0: # this occurs on draw
            return 0
        else:
            return -1

    def alpha_beta_search(self, game, player):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.get_successors(game)
        #print("e")
        # print(successors)
        best_state = None # will be tuple of x y coordinates for best move
        for state in successors:
            game_cp = self.copy_game(game)
            #print("cur state: ", state)
            game_cp.make_move(state[1])
            game_cp.last_moved_i = state[0]
            game_cp.last_moved_j = state[1]
            new_player = self.next_player(player)
            value = self.min_value(game_cp, new_player, best_val, beta)
            #print("value: ",value)
            if value > best_val:
                best_val = value
                best_state = state
        # print("best state: ", best_state)
        return best_state

    def max_value(self, game, player, alpha, beta):
        #print('hello')
        if self.is_terminal(game):
            score = self.get_score(game)
            #print("my score: ", score)
            return score
        infinity = float('inf')
        value = -infinity

        successors = self.get_successors(game)
        #print("breaking suc: ", successors)
        count = 0
        for state in successors:
            game_cp = self.copy_game(game)
            count += 1
            # print(count)
            # print(count, "maybe breaks")
            # print(game_cp.board)
            game_cp.make_move(state[1]) # breaks here
            #print(count, "maybe breaks")
            game_cp.last_moved_i = state[0]
            game_cp.last_moved_j = state[1]
            new_player = self.next_player(player)
            value = max(value, self.min_value(game_cp, new_player, alpha, beta))
            #print("max val: ", value)
            if value >= beta:
                #print(value)
                return value
            alpha = max(alpha, value)
            #print("down")
        return value

    def min_value(self, game, player, alpha, beta):
        if self.is_terminal(game):
            return self.get_score(game)
        infinity = float('inf')
        value = infinity

        successors = self.get_successors(game)
        #print(successors)
        for state in successors:
            game_cp = self.copy_game(game)
            game_cp.make_move(state[1])
            game_cp.last_moved_i = state[0]
            game_cp.last_moved_j = state[1]
            new_player = self.next_player(player)
            value = min(beta, self.max_value(game_cp, new_player, alpha, beta))
            #print("min val: ", beta)
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def find_legal_move(self, timeout=None):
        move = None
        if self.game.get_winner() == None:
            try:
                game_cp = self.copy_game(self.game)
                move = self.alpha_beta_search(game_cp, self.player)
                # print("my move: ", move)
                if move == None:
                    raise Exception('No possible AI moves')

            except Exception as e:
                print('randomai',e)
        if move != None:
            self.made_moves.append(move)
        # print(move)
        return move # this will be best possible row and column move

    def get_last_found_move(self):
        return self.made_moves[-1]
