################################################################################
# FILE : game.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: File contains Game logic for the 4 in a row game.
################################################################################

class Error(Exception):
    pass

class IllegalMove(Error):
    """Raised when illegal move attempted"""
    pass

class IllegalLoacation(Error):
    """Raised when Illegal coordinate is searched for"""
    pass

class Game:
    GAME_COUNT = 0
    GAME_DRWAW = 0 # Value returned if get_win function finds game Draw.
    COLUMN_NUM = 7
    ROW_NUM = 6
    def __init__(self):
        """ Constructor for game logic"""
        self.game_over = None
        self.winning_disks = []
        self.last_moved_i = 0
        self.last_moved_j = 0
        self.board = []
        for i in range(6):
            row = []
            for j in range(7):
                row.append(None)
            self.board.append(row)


    def column_full(self,column):
        """Function checks if selected column is full. Returns False if not full and True if full."""
        for i in range(self.ROW_NUM):
            if self.board[i][column] == None: return False
        return True


    def make_move(self, column):
        """ Function used place a disk in selected column. Function checks weather selected move can be made.
        If move is possible then function replaces None with relevant player disk on the game board. If move
        is not possible (either because game is over, col out of bounds or column is full) function raises
        IllegalMove error"""
        if column>6 or column<0 or self.column_full(column) or self.game_over != None:
            raise IllegalMove
        else:
            player = self.get_current_player()
            for i in range(5,-1,-1):
                if self.board[i][column] == None:
                    self.board[i][column] = player
                    self.last_moved_i = i
                    self.last_moved_j = column
                    self.GAME_COUNT += 1
                    return
                else: i-= 1


    def down(self,last_i,last_j,player):
        """Helper function to get winner.Function checks weather player has 4 consecutive disks down the column
        of the last disk added. If found, function will return True and update the winning discs.
        Else function will return False."""
        winning_disks = []
        if last_i + 3 <= 5:
            for i in range(4):
                if self.board[last_i + i][last_j] == player:
                    winning_disks.append((last_i+i,last_j))
            if len(winning_disks)==4:
                self.winning_disks = winning_disks
                return True
        return False


    def left_right(self,last_i,last_j,player):
        """
        Function checks whether 4 consecutive disks can be found horizontally from last j coord placed.
        Function checks first left (appending matching disks) and then right. If 4 are found will return true and
        update the winning disks. Else will return False.
        :param last_i: last i coordinate placed on board
        :param last_j: last j coordinate placed on board
        :param player: player who made the move
        :return: True if consecutive disks have been found, False otherwise.
        """
        #Left
        j = last_j
        winning_disks = []
        while j>=0 and self.board[last_i][j] == player and len(winning_disks)<4:
            winning_disks.append((last_i,j))
            j-=1
        if len(winning_disks) == 4:
            self.winning_disks = winning_disks
            return True
        #Right
        j= last_j+1
        while j <=6  and self.board[last_i][j] == player and len(winning_disks) < 4:
            winning_disks.append((last_i, j))
            j += 1
        if len(winning_disks) == 4:
            self.winning_disks = winning_disks
            return True
        return False


    def up_left_down_right(self,last_i,last_j,player):
        """
        Checks weather 4 matching disks can be found diagonally (up_left and down right) from last disk placed.
        Function first performs up_left search and then down_right search. If 4 consecutive disks found then
        function will update the winning disks and return True. Else will return False.
        :param last_i: last i placed on board
        :param last_j: last j placed on board
        :param player: player who made the move
        :return: True if 4 consecutive found, False otherwise
        """
        # up_Left search
        winning_disks = []
        j = last_j
        i = last_i
        while j >= 0  and i>=0 and self.board[i][j] == player and len(winning_disks) < 4:
            winning_disks.append((i, j))
            j -= 1
            i-=1
        if len(winning_disks) == 4:
            self.winning_disks = winning_disks
            return True

        #down_right search
        if j <= 5 and i <=4:
            j = last_j + 1
            i= last_i+1
        while j <=6 and i<=5 and self.board[i][j] == player and len(winning_disks) < 4:
            winning_disks.append((i, j))
            j += 1
            i+=1
        if len(winning_disks) == 4:
            self.winning_disks = winning_disks
            return True
        return False

    def up_right_down_left(self, last_i, last_j, player):
        """
        Checks weather 4 matching disks can be found diagonally (up_right and down_left) from last disk placed.
        Function first performs up_right search and then down_left search. If 4 consecutive disks found then
        function will update the winning disks and return True. Else will return False.
        :param last_i: last i placed on board
        :param last_j: last j placed on board
        :param player: player who made the move
        :return: True if 4 consecutive found, False otherwise
        """
        # up_right search
        winning_disks = []
        j = last_j
        i = last_i
        while j <=6 and i >= 0 and self.board[i][j] == player and len(winning_disks) < 4:
            winning_disks.append((i, j))
            j += 1
            i -= 1
        if len(winning_disks) == 4:
            self.winning_disks = winning_disks
            return True

        # down left search
        if j>=1 and i<=4:
            j = last_j - 1
            i = last_i + 1
        while j >=0  and i <=5  and self.board[i][j] == player and len(winning_disks) < 4:
            winning_disks.append((i, j))
            j -= 1
            i += 1
        if len(winning_disks) >= 4:
            self.winning_disks = winning_disks
            return True
        return False





    def get_winner(self):
        """Uses helper functions to determine weather one of the players has won the game. If any one of the
        search directions returns True then the game has been won by the current player. Alternatively if the last
        move has created a board that is full and no player has won function will return 'Draw'. If neither
        of these is True function returns None (meaning game can continue)"""
        last_i = self.last_moved_i
        last_j = self.last_moved_j
        my_p = self.get_current_player()
        if my_p == 1: player =2
        elif my_p ==2: player = 1
        down = self.down(last_i,last_j,player)
        left_right = self.left_right(last_i,last_j,player)
        up_left_down_right = self.up_left_down_right(last_i,last_j,player)
        up_right_down_left = self.up_right_down_left(last_i,last_j,player)
        if down or left_right or up_left_down_right or up_right_down_left:
            self.game_over = player
            return player
        for i in range(self.ROW_NUM):
            for j in range(self.COLUMN_NUM):
                if self.board[i][j] == None: return None
        self.game_over = self.GAME_DRWAW
        return self.GAME_DRWAW


    def get_player_at(self, row, col):
        """Function checks which player is at required search location. If invalid row/column requested
        function will raise IllegaLocation error. Other wise will return relevant player at board location
        (or None) if no player is in Searched location."""
        if row<0 or row>5 or col<0 or col>6:
            raise IllegalLoacation
        elif self.board[row][col] == 1: return 1
        elif self.board[row][col] == 2: return 2
        else: return None

    def get_current_player(self):
        """Function returns current player, uses Game count to alternate between odd and even moves
        and differentiate between the 2 players."""
        if self.GAME_COUNT%2 == 0:
            return 1
        else:
            return 2



