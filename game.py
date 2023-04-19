class Game:
    # Initialize the Game class with an id
    def __init__(self, id):
        self.id = id  # The unique ID of the game
        self.board = [" " for _ in range(9)]
        self.ready = False  # Whether both players are connected to the game (False initially)
        self.choices = [None, None]
        self.p1Moves = set()
        self.p2Moves = set()
        self.current_player = "X"
        self.exit = False

    def get_board(self):
        return self.board

    def is_full(self):
        return all(cell != " " for cell in self.board)

    # check winner
    def winner(self):
        win_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        winner = -1
        for position in win_positions:
            position_set = set(position)
            if self.get_first_player() == 0:
                if position_set.issubset(self.p1Moves):
                    winner = 0
                    break
                if position_set.issubset(self.p2Moves):
                    winner = 1
                    break
            else:
                if position_set.issubset(self.p1Moves):
                    winner = 1
                    break
                if position_set.issubset(self.p2Moves):
                    winner = 0
                    break
        return winner

    def check_valid_move(self, position):
        return self.board[position] == " "

    # record a player's move:
    def play(self, player, position):
        position = int(position)
        if player == self.get_first_player():
            self.board[position] = "X"
            self.p1Moves.add(position)
            self.current_player = "O"
        else:
            self.board[position] = "O"
            self.p2Moves.add(position)
            self.current_player = "X"

            # check if both players are connected

    def connected(self):
        return self.ready

    def game_over(self):
        if self.is_full() or self.winner() != -1:
            return True
        return False

    # Replaying the game and resetting the game environment should take place
    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.p1Moves = set()
        self.p2Moves = set()
        self.current_player = "X"
        self.choices = [None, None]
        self.exit = False

    def exit_game(self):
        self.exit = True

    def make_choice(self, player, decision):
        self.choices[player] = decision

    def get_first_player(self):
        first_player = -1
        if self.choices == ["agree", "agree"]:
            first_player = 0
        elif self.choices == ["disagree", "disagree"]:
            first_player = 1
        return first_player

    def reset_choices(self):
        self.choices = [None, None]


