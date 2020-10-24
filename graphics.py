################################################################################
# FILE : graphics.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: File contains main GUI class. GUI includes all the graphics used
#              for user interface with the game.
################################################################################

import tkinter as tk
import game as g
import ai
import random as rand

HEIGHT = 600
WIDTH= 700
COLUMNS = 7
ROWS = 6
PLAYER1 = 1
PLAYER2 = 2
P1_SELECT = 'Select player 1 type:'
P2_SELECT = 'Select player 2 type:'
TITLE_MSG = 'FOUR IN A ROW'
BG_COLOUR = 'mint cream'
COLOURS = ('white','red')
FONT = "times new roman"
TITLE_TXT_SIZE = 50
COLUMN_HEIGHT = 575
COLUMNS_WIDTH = 75
DISK_HEIGHT = 75
DISK_WIDTH = 75
BOARD_COLOUR = 'blue'
DISK_COORD = 5,5,75,75
PLAYER_1_COL = 'red'
PLAYER_2_COL='green'
WIN_COL = 'gold'
DISK_N0 = 1
ILLEGAL_MSG = "Illegal move!"
DRAW_MSG = 'Game Draw'
HUMAN_PLAYER = 'Human'
AI_PLAYER = "AI"
WAIT_TIME = 1000


class GUI:
    """Class contains graphics of the Game and the interface through which Game user can interact with
    the game logic and chose player types"""
    def __init__(self,root):
        """Constructor for GUI"""
        self.root = root
        self.player1 = None
        self.player2 = None
        self.game = g.Game()
        self.can_play = False #Used to block Illegal user moves at start and during AI turn
        self.used_disks = []

        self.canvas = tk.Canvas(self.root,width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
        self.canvas_board = []
        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                row.append(None)
            self.canvas_board.append(row)

        self.msg_frame = tk.Frame(self.canvas)
        self.msg_can = tk.Canvas(self.msg_frame, height=15, width=200, bg=BG_COLOUR)
        self.error_msg = tk.Label(self.msg_can, text=ILLEGAL_MSG, bg=BG_COLOUR, font=(FONT, 20))
        self.msg_can.pack(side=tk.TOP)
        self.initial_board()
        self.msg_frame.pack()
        self.canvas.pack()

    def get_game_player(self,player):
        """Function used to determine the 'type' of player 1 and player 2"""
        if player == 1:
            return self.player1
        if player == 2:
            return self.player2


    def only_AI(self):
        """Checks if player has selected only AI players, in this case clicking will have no
        effect on the game."""
        if self.player1 == AI_PLAYER and self.player2 == AI_PLAYER:
            return True


    def start_menu(self):
        """Initial menu that appears at head of canvas. Includes title and the options to select player 1
        and player 2 types"""
        start_frame = tk.Frame(self.canvas,bg=BG_COLOUR)
        player1_frame = tk.Frame(start_frame,bg=BG_COLOUR)

        # Parameters used to control Radiobuttons. Each radio button controlled by different variable.

        self.var1 = tk.IntVar()
        self.var2= tk.IntVar()
        self.var3= tk.IntVar()
        self.var4 = tk.IntVar()
        p1_title = tk.Label(player1_frame, fg=PLAYER_1_COL, text=P1_SELECT, bg=BG_COLOUR, font=(FONT,20),padx=10)
        self.p1_option1 = tk.Radiobutton(player1_frame, text='Human',bg=BG_COLOUR,
                                    command=lambda :self.player_human(PLAYER1,self.p1_option1,self.p1_option2),
                                    variable=self.var1)
        self.p1_option2 = tk.Radiobutton(player1_frame, text='AI',bg=BG_COLOUR,
                                    command=lambda :self.player_ai(PLAYER1,self.p1_option1,self.p1_option2),
                                    variable=self.var2)
        self.p1_option2.deselect()

        player2_frame = tk.Frame(start_frame,bg=BG_COLOUR)
        p2_title = tk.Label(player2_frame, fg= PLAYER_2_COL, text=P2_SELECT, bg=BG_COLOUR, font=(FONT, 20),padx=10)
        self.p2_option1 = tk.Radiobutton(player2_frame, text='Human',bg=BG_COLOUR,
                                    command=lambda :self.player_human(PLAYER2,self.p2_option1,self.p2_option2),
                                    variable=self.var3)

        self.p2_option1.deselect()
        self.p2_option2 = tk.Radiobutton(player2_frame, text='AI',bg=BG_COLOUR,
                                    command=lambda:self.player_ai(PLAYER2,self.p2_option1,self.p2_option2),
                                         variable=self.var4)
        player1_frame.pack(side=tk.LEFT)
        p1_title.pack(side=tk.TOP)
        self.p1_option1.pack(side=tk.TOP)
        self.p1_option2.pack(side=tk.TOP)

        player2_frame.pack(side=tk.LEFT)
        p2_title.pack(side=tk.TOP)
        self.p2_option1.pack(side=tk.TOP)
        self.p2_option2.pack(side=tk.TOP)

        # Start button used to initialize game once players have been selected.
        ind = rand.randint(0, 1)
        colour = COLOURS[rand.randint(0, 1)]
        start_button = tk.Button(start_frame,text='start',bg=colour,command= lambda :self.initialize_game())
        start_button.pack(side=tk.BOTTOM)
        start_frame.pack(side=tk.TOP)


    def initialize_game(self):
        """Once start has been pressed, if player 1 is AI then function will place the first disk on the
        board. Will only work once both player types have been selected."""
        if self.player1 != None and self.player2 != None:
            if self.only_AI() != True:
                self.can_play = True
            if self.player1 == AI_PLAYER:
                self.root.after(WAIT_TIME,lambda :self.ai_move())




    def player_human(self,player_no,option1,option2):
        """
        Function used to set player type. Function called if user has selected player type to be HUMAN.
        Once type has been selected the function disables radio buttons to prevent further changes from being
        made throughout the course of the game.
        :param player_no: either player 1 or player 2
        :param option1: Set player as HUMAN
        :param option2: Set player as AI
        :return: Sets self.player as selected by user.
        """
        option1.configure(state=tk.DISABLED)
        option2.configure(state=tk.DISABLED)
        if player_no==1:
            self.player1 = HUMAN_PLAYER
        else:
            self.player2 = HUMAN_PLAYER


    def player_ai(self,player_no,option1,option2):
        """
          Function used to set player type. Function called if user has selected player type to be AI.
          Once type has been selected the function disables radio buttons to prevent further changes from being
            made throughout the course of the game.
          :param player_no: either player 1 or player 2
          :param option1: Set player as HUMAN
          :param option2: Set player as AI
          :return: Sets self.player as selected by user.
          """
        option1.configure(state=tk.DISABLED)
        option2.configure(state=tk.DISABLED)
        if player_no==1:
            self.player1 = AI_PLAYER
            self.ai_player = player_no
        else:
            self.player2 = AI_PLAYER
            self.ai_player = player_no


    def initial_board(self):
        """Function sets up the initial game Board and creates widges such as title and board canvas.
        To create board Graphic function first creates columns and then fills each of these columns with
        rows of disk squares."""
        title_frame = tk.Frame(self.canvas)
        title_frame.pack(side=tk.TOP)
        self.start_menu()
        title = tk.Label(title_frame, fg="blue", text=TITLE_MSG, bg=BG_COLOUR, font=(FONT,TITLE_TXT_SIZE))
        title.pack(side=tk.TOP)
        middle_frame = tk.Frame(self.canvas)
        middle_frame.pack(side=tk.TOP)

        # Once columns have been created, rows are added into each column.
        for j in range(COLUMNS):
            col = tk.Canvas(middle_frame,bg=BOARD_COLOUR,height=COLUMN_HEIGHT,width=COLUMNS_WIDTH)
            self.create_disk(col,j)
            col.pack(side=tk.LEFT)


    def create_disk(self,col,j):
        """Function draws disk circles in each of the grid squares and 'binds' them to the human move
        function, meaning that when clicked on, each square indicates a user selection of where to
        place their next disk."""
        for i in range(ROWS):
            new_disk = tk.Canvas(col,height=DISK_HEIGHT,width=DISK_WIDTH,bg=BOARD_COLOUR)
            new_disk.pack(side=tk.TOP)
            self.canvas_board[i][j] = new_disk
            new_disk.bind('<Button-1>',lambda click:self.human_move(i,j)) # Binding each disk to action.
            self.canvas_board[i][j].create_oval((DISK_COORD),fill=BG_COLOUR)



    def human_move(self,i,j):
        """Function called when disk is clicked on. Function will attempt to place a disk on the
        selected column. Game will only 'progress' (ie. count +=1 and next player turn) if disk
        placement is successfull"""
        if self.only_AI() == True: return
        if self.can_play == True: # This turned off during AI move and before player types have been selected.
            player_no = self.game.get_current_player()
            success = self.add_disk(player_no,i,j)
            if self.game.game_over == None and success != False:
                player_no = self.game.get_current_player()
                player = self.get_game_player(player_no)

                # Triggers AI move if next player is AI. Otherwise waits for next click.
                if player == AI_PLAYER:
                    self.can_play = False
                    self.root.after(WAIT_TIME, lambda: self.ai_move())


    def ai_move(self):
        """Function performs AI move. Called on depending on player type of current player. afer function
        used to delay movement and allow user to follow the progress of the game."""
        if not self.game.game_over: # Prevents moves being made after game is over
            player_no = self.game.get_current_player()
            my_ai = ai.AI(self.game,player_no)
            possible_move = my_ai.find_legal_move()
            j= possible_move
            i = 5
            while (i,j) in self.used_disks and i>=0:
                i -= 1
            self.add_disk(player_no,i,j)
            if self.player1 == AI_PLAYER and self.player2 == AI_PLAYER:
                self.root.after(WAIT_TIME,lambda :self.ai_move())
            if self.only_AI() != True:
                self.can_play = True # Turned back on to allow human to make next move.


    def add_disk(self,player,i,j):
        """Function that attempts to add disk to board based on either human or AI move.
        If move is legal then it will change slected disk to appropriate player colour.
        If Illegal move attempted then will raise error and return False."""
        if player == 1:
            colour = PLAYER_1_COL
        elif player == 2:
            colour = PLAYER_2_COL
        while (i, j) in self.used_disks and i>=0:
            i -= 1
        try:
            self.game.make_move(j)
            self.game.last_moved_i = i
            self.game.last_moved_j = j
            self.used_disks.append((i, j))
            self.canvas_board[i][j].itemconfig(DISK_N0, fill=colour)
            self.error_msg.pack_forget()
            winner = self.game.get_winner()
            if winner != None:
                self.highlight_winner()
                self.end_menu(winner)

        # Move is considered Illegal if column is out of bounds or already full.
        except g.IllegalMove:
            self.error_msg.pack()
            return False



    def highlight_winner(self):
        """ Changes the colour of the disks in self.winning disks."""
        for coord in self.game.winning_disks:
            self.canvas_board[coord[0]][coord[1]].itemconfig(DISK_N0, fill=WIN_COL)




    def reset(self,window):
        """Function resets the game board and the GUI graphic display. All parameters (including menu for
        player types, game board and Game count) are reset."""
        window.destroy()
        self.player1 = None
        self.player2 = None
        self.used_disks = []
        self.game.last_moved_i,self.game.last_moved_j = 0,0
        self.can_play = False
        self.game.game_over = None
        self.game.winning_disks = []
        self.game.GAME_COUNT = 0

        # Resets Radoibuttons controlling player type selection.
        self.var1,self.var2,self.var3,self.var4 = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
        self.p1_option1.configure(state=tk.NORMAL,variable= self.var1)
        self.p1_option2.configure(state=tk.NORMAL,variable= self.var2)
        self.p2_option1.configure(state=tk.NORMAL,variable=self.var3)
        self.p2_option2.configure(state=tk.NORMAL,variable=self.var4)


        # Resets game board and and disk colours in the GUI graphic board.
        for i in range(self.game.ROW_NUM):
            for j in range(self.game.COLUMN_NUM):
                self.game.board[i][j] = None
                self.canvas_board[i][j].itemconfig(DISK_N0, fill=BG_COLOUR)


    def end_menu(self,player):
        """Pop up window displaying either option to play again or to exit the game. If user choses
        to play again then reset function is triggered."""
        wnd = tk.Tk()
        wnd_canvas = tk.Canvas(wnd,height=400,width=400,bg=BG_COLOUR)
        wnd_canvas.pack()
        wnd_title = tk.Label(wnd_canvas, fg="blue", text=TITLE_MSG, bg=BG_COLOUR, font=(FONT,TITLE_TXT_SIZE))
        wnd_title.pack(side=tk.TOP)
        if self.game.get_winner() == 0:
            draw_msg = tk.Label(wnd_canvas, text=DRAW_MSG,
                                bg=BG_COLOUR, font=(FONT, 20))
            draw_msg.pack(side=tk.TOP)
        else:
            win_msg = tk.Label(wnd_canvas, text='Player ' + str(player) + ' wins!',
                               bg=BG_COLOUR, font=(FONT, 20))
            win_msg.pack(side=tk.TOP)
        play_again = tk.Button(wnd_canvas,text='Play again?',command=lambda :self.reset(wnd))
        play_again.pack(side=tk.LEFT)
        exit = tk.Button(wnd_canvas,text='EXIT?',command=lambda :self.exit(wnd))
        exit.pack(side=tk.RIGHT)

    def end_msg(self, player):
        """ Displayed when game is over. Will either display which player has won or present a DRAW
        message if the board is full and no player has won."""
        self.msg_can.pack()
        if self.game.get_winner() == 0:
            draw_msg = tk.Label(self.msg_can, text=DRAW_MSG,
                                bg=BG_COLOUR, font=(FONT, 20))
            draw_msg.pack()
        else:
            win_msg = tk.Label(self.msg_can, text='Player ' + str(player) + ' wins!',
                               bg=BG_COLOUR, font=(FONT, 20))
            win_msg.pack()
        self.end_menu()


    def exit(self, window):
        """Exits the game"""
        window.destroy()
        self.root.destroy()


