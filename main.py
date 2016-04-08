import random


class Player(object):
    def __init__(self, character):
        self.character = character


class Human(Player):
    def go(self, board):
        while True:
            column = int(input('Column: '))

            if board.insert(column, self.character):
                return True


class Ai(Player):
    def go(self, board):
        print('im thinking very hard....')
        while True:
            if board.insert(random.randint(0, 6), self.character):
                return True


class Board(object):
    def __init__(self):
        # initialize board of 6 rows by 7 columns to empty spaces
        # let's try it column major. this will make it easier to insert a piece
        self.board = [[] for i in range(0, 7)]
        for i in range(0, 7):
            self.board[i] = [' ' for j in range(0, 6)]

    def display(self):
        # display is a little trickier due to the column major nature we are attempting

        # display column numbers
        print([str(i) for i in range(0, len(self.board))])

        for i in range(len(self.board[0]) - 1, -1, -1):
            print([self.board[j][i] for j in range(0, len(self.board))])

    def insert(self, column, piece):
        """
        attempt to place piece into board in column
        :param column: index of column to place. 0 indexed
        :param piece: character to place into column
        :return: True if piece was put into board. False otherwise
        """

        # bounds check
        if column > 6 or column < 0:
            return False

        for i in range(0, 6):
            if ' ' == self.board[column][i]:
                self.board[column][i] = piece
                return True

        return False

    def filled(self):
        for i in range(0, len(self.board)):
            if any(map(lambda x: x == ' ', self.board[i])):
                return False

        return True

    def won_by(self, piece):
        # match by column
        if any(map(lambda x: self.match_four(x, piece), self.board)):
            return True

        # match by row
        for i in range(0, len(self.board[0])):
            row = [self.board[j][i] for j in range(0, len(self.board))]
            if self.match_four(row, piece):
                return True

        # match by diagonal
        for i in range(0, len(self.board)): # for each column
            for j in range(0, len(self.board[i])): # for each constituent
                # look north west
                if self.contains(i - 3, j - 3):
                    # construct list to pass to match_four
                    if self.match_four([self.board[i - k][j - k] for k in range(0, 4)], piece):
                        return True

                # look north east
                if self.contains(i + 3, j - 3):
                    if self.match_four([self.board[i + k][j - k] for k in range(0, 4)], piece):
                        return True

                # etc
                if self.contains(i - 3, j + 3):
                    if self.match_four([self.board[i - k][j + k] for k in range(0, 4)], piece):
                        return True

                # etc again
                if self.contains(i + 3, j + 3):
                    if self.match_four([self.board[i + k][j + k] for k in range(0, 4)], piece):
                        return True

    def contains(self, col, row):
        if col < 0 or col >= len(self.board):
            return False
        elif row < 0 or row >= len(self.board[0]):
            return False
        else:
            return True


    def match_four(self, arr, piece):
        num = 0
        for i in range(0, len(arr)):
            if piece == arr[i]:
                num += 1
                if 4 == num:
                    return True
            else:
                num = 0

        return num == 4


if __name__ == '__main__':
    players = [Human('R'), Ai('B')]
    board = Board()

    player_index = 0

    while not board.filled():
        board.display()

        current_player = players[player_index]

        current_player.go(board)

        # a game can only be won by a player on their own turn
        if board.won_by(current_player.character):
            board.display()
            print("Player " + current_player.character + " has won the game!")
            exit()

        player_index = (player_index + 1) % 2

