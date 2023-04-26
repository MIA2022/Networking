class Game:
    def __init__(self, id):
        self.p1Went = [False,False,False,False,False]
        self.p2Went = [False,False,False,False,False]
        self.ready = False
        self.id = id
        self.move1 = set()
        self.move2 = set()
        self.round = 0
        self.choices = [None, None]
        self.exit = False
        self.game_result = -1
        # self.game_reset = [False,False]
        # self.game_board = [" " for _ in range(9)]
    
    def make_reset(self, player):
        if player == 0:
            self.game_reset = [True, False]
        elif player ==1:
            self.game_reset = [False, True]


    
    def match_board(self, position):
        if position == "7":
            return 0
        elif position == "8":
            return 1
        elif position == "9":
            return 2
        elif position == "4":
            return 3
        elif position == "5":
            return 4
        elif position == "6":
            return 5
        elif position == "1":
            return 6
        elif position == "2":
            return 7
        elif position == "3":
            return 8
        elif position == 0:
            return "7"
        elif position == 1:
            return "8"
        elif position == 2:
            return "9"
        elif position == 3:
            return "4"
        elif position == 4:
            return "5"
        elif position == 5:
            return "6"
        elif position == 6:
            return "1"
        elif position == 7:
            return "2"
        elif position == 8:
            return "3"
    
    def get_board(self):
        return self.game_board

    def make_choice(self, p, decision):
        if p==0:
            self.choices = [decision, 'agree']
        else:
            self.choices = ['agree', decision]



    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        if p == 0:
            return self.move1
        else:
            return self.move2

    def play(self, player, move):
            # print("player, move", player, move, type(move))
            # position=self.match_board(move)
            # print("position", position)
            if player ==0:
                self.p1Went[self.round] = True
                # self.game_board[position] = "X"
                self.move1.add(move)
            else:
                self.p2Went[self.round] = True
                # self.game_board[position] = "O"        
                self.move2.add(move)
                self.round+=1


    def connected(self):
        return self.ready
    
    def exit_game(self):
        self.exit = True

    def bothWent(self):
        return self.p1Went[self.round] and self.p2Went[self.round]

    def winner(self):
        winner = -1
        if "1"  in self.move1 and "2" in self.move1 and "3" in self.move1:
            winner = 1
        elif "4"  in self.move1 and "5" in self.move1 and "6" in self.move1:
            winner = 1
        elif "7"  in self.move1 and "8" in self.move1 and "9" in self.move1:
            winner = 1
        elif "1"  in self.move1 and "4" in self.move1 and "7" in self.move1:
            winner = 1
        elif "2"  in self.move1 and "5" in self.move1 and "8" in self.move1:
            winner = 1  
        elif "3"  in self.move1 and "6" in self.move1 and "9" in self.move1:
            winner = 1
        elif "1"  in self.move1 and "5" in self.move1 and "9" in self.move1:
            winner = 1
        elif "3"  in self.move1 and "5" in self.move1 and "7" in self.move1:
            winner = 1
        elif "1"  in self.move2 and "2" in self.move2 and "3" in self.move2:
            winner = 2
        elif "4"  in self.move2 and "5" in self.move2 and "6" in self.move2:
            winner = 2
        elif "7"  in self.move2 and "8" in self.move2 and "9" in self.move2:
            winner = 2
        elif "1"  in self.move2 and "4" in self.move2 and "7" in self.move2:
            winner = 2
        elif "2"  in self.move2 and "5" in self.move2 and "8" in self.move2:
            winner = 2 
        elif "3"  in self.move2 and "6" in self.move2 and "9" in self.move2:
            winner = 2
        elif "1"  in self.move2 and "5" in self.move2 and "9" in self.move2:
            winner = 2
        elif "3"  in self.move2 and "5" in self.move2 and "7" in self.move2:
            winner = 2
        elif self.round == 4 and self.p1Went[4]:
            winner = 0
        self.game_result = winner
        return winner

    def resetWent(self):
        for a in len(self.p1Went):
            self.p1Went[a] = False
        for b in len(self.p1Went):
            self.p1Went[b] = False
        self.move1 = set()
        self.move2 = set()
        self.round = 0
        self.choices = [None, None]
        self.exit = False
        self.game_result = -1
        self.ready=True
        # self.game_board = [" " for _ in range(9)]




   
