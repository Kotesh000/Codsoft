import sys
import pygame
from constants import *
import numpy as np
import random
import copy

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(Back_Ground_Color)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_state(self):
        '''
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        '''
        # Vertical wins
        for column in range(COLUMNS):
            if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
                return int(self.squares[0][column])

        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return int(self.squares[row][0])

        # Desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return int(self.squares[1][1])

        # Asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return int(self.squares[1][1])

        # No win yet
        return 0

    def mark_sqr(self, row, column, player):
        self.squares[row][column] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, column):
        return self.squares[row][column] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.empty_sqr(row, column):
                    empty_sqrs.append((row, column))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]  # [row, column]

    def minimax(self, board, maximizing):
        # Terminal case
        case = board.final_state()
        # Player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # Player 2 wins
        if case == 2:
            return -1, None

        # Draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, column) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, column, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, column)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, column) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, column, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, column)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            move = self.rnd(main_board)
        else:
            # Minimax algo choice
            eval, move = self.minimax(main_board, False)
            print(f'AI has chosen to mark the square in position {move} with an eval of {eval}')
        return move  # row, column


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1-circles, 2-cross
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        # Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, column):
        if self.player == 1:
            # Draw cross
            # Desc line
            start_desc = (column * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # Asc line
            start_asc = (column * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # Draw circle
            center = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1


def main():
    # Object
    game = Game()
    board = game.board
    ai = game.ai

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                column = pos[0] // SQSIZE

                if board.empty_sqr(row, column):
                    board.mark_sqr(row, column, game.player)
                    game.draw_fig(row, column)
                    winner = board.final_state()
                    if winner:
                        print(f"Player {winner} wins!")
                        pygame.quit()
                        sys.exit()
                    elif board.isfull():
                        print("It's a draw!")
                        pygame.quit()
                        sys.exit()

                    game.next_turn()

            if game.gamemode == 'ai' and game.player == ai.player:
                # Update the screen
                pygame.display.update()

                # AI methods
                row, column = ai.eval(board)

                board.mark_sqr(row, column, ai.player)
                game.draw_fig(row, column)
                winner = board.final_state()
                if winner:
                    print(f"Player {winner} wins!")
                    pygame.quit()
                    sys.exit()
                elif board.isfull():
                    print("It's a draw!")
                    pygame.quit()
                    sys.exit()

                game.next_turn()

        pygame.display.update()


if __name__ == "__main__":
    main()
