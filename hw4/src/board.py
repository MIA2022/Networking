import pygame


class Board:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def draw(self, win, board):
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(win, (0, 0, 128),
                                 (self.x + col * self.cell_size, self.y + row * self.cell_size,
                                  self.cell_size, self.cell_size), 3)
                position = row * 3 + col
                if board[position] != ' ':
                    self.draw_x_o(win, row, col, board)

    def draw_x_o(self, win, row, col, board):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render(board[row * 3 + col], 1, (255, 165, 0))
        win.blit(text, (self.x + col * self.cell_size + self.cell_size // 2 - text.get_width() // 2,
                        self.y + row * self.cell_size + self.cell_size // 2 - text.get_height() // 2))

    def click(self, pos):
        mouse_x = pos[0]
        mouse_y = pos[1]
        if mouse_x < self.x or mouse_y < self.y or mouse_x > self.x + 3 * self.cell_size or mouse_y > self.y + 3 * self.cell_size:
            print("None")
            return None
        row = (mouse_y - self.y) // self.cell_size
        col = (mouse_x - self.x) // self.cell_size
        position = row * 3 + col
        return position