import sys
import pprint

class BingoGame:
    def __init__(self):
        self.draw_index = -1
        self.draw_pile = None
        self.boards = []

    def load_state(self, lines):
        current_board = None

        for line in lines:
            line = line.strip()
            if not line:
                if current_board:
                    self.boards.append(current_board)
                current_board = None
                continue

            if self.draw_pile is None:
                self.draw_pile = [int(x) for x in line.split(',')]
                continue

            if not current_board:
                current_board = []

            current_board.append([(int(x), 0) for x in line.split()])

        if current_board:
            self.boards.append(current_board)

    def check_winners(self):
        return [b for b in self.boards if self.check_board_winner(b)]

    def draw(self):
        self.draw_index += 1
        return self.draw_pile[self.draw_index]

    def can_draw(self):
        return (self.draw_index+1) < len(self.draw_pile)

    def apply_draw(self, draw):
        for board in self.boards:
            for row in board:
                for i, spot in enumerate(row):
                    if spot[0] == draw:
                        row[i] = (spot[0], 1)

    def score(self, board):
        return self.draw_pile[self.draw_index] * sum([sq[0] for row in board for sq in row if sq[1] == 0])

    @staticmethod
    def check_board_winner(board):
        for direction in (board, zip(*board)):
            for row in direction:
                if all(cell[1] for cell in row):
                    return True
        return False

    def __repr__(self):
        return f'Bingo(len(boards)={len(self.boards)}, next_draw={self.draw_pile[self.draw_index]})'


def main(input):
    game = BingoGame()
    game.load_state(input.readlines())

    while game.can_draw() and len(game.boards) >= 1:
        game.apply_draw(game.draw())
        winners = game.check_winners()
        for winner in winners:
            print(f"Removing winner with score={game.score(winner)}")
            game.boards.remove(winner)

        print(f"Boards remaining: {len(game.boards)}")

    # pprint.pprint(winners)
    # for winner in winners:
    #     print(game.score(winner))


if __name__ == '__main__':
    main(sys.stdin)