from Piece import Piece
from cell import Cell


class Board:
    def __init__(self):
        self.cells = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Cell((i, j)))
                if i == 1:
                    row[j].set_piece(Piece.BLACKPAWN)
                elif i == 0:
                    if j == 0 or j == 7:
                        row[j].set_piece(Piece.BLACKROOK)
                    elif j == 1 or j == 6:
                        row[j].set_piece(Piece.BLACKKNIGHT)
                    elif j == 2 or j == 5:
                        row[j].set_piece(Piece.BLACKBISHOP)
                    elif j == 3:
                        row[j].set_piece(Piece.BLACKQUEEN)
                    elif j == 4:
                        row[j].set_piece(Piece.BLACKKING)
                if i == 6:
                    row[j].set_piece(Piece.WHITEPAWN)
                elif i == 7:
                    if j == 0 or j == 7:
                        row[j].set_piece(Piece.WHITEROOK)
                    elif j == 1 or j == 6:
                        row[j].set_piece(Piece.WHITEKNIGHT)
                    elif j == 2 or j == 5:
                        row[j].set_piece(Piece.WHITEBISHOP)
                    elif j == 3:
                        row[j].set_piece(Piece.WHITEQUEEN)
                    elif j == 4:
                        row[j].set_piece(Piece.WHITEKING)

            self.cells.append(row)

        self.update_checked(True)

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.cells[i][j].piece.value, end='')
            print('\n')

    def print_checked(self):
        for i in range(8):
            for j in range(8):
                if self.cells[i][j].white_checked and self.cells[i][j].black_checked:
                    print('A', end='')
                elif self.cells[i][j].white_checked:
                    print('W', end='')
                elif self.cells[i][j].black_checked:
                    print('B', end='')
                else:
                    print('-', end='')
            print()

    def move(self, move, turn):
        fromX = move[0]
        fromY = move[1]
        toX = move[2]
        toY = move[3]

        legal = self.generate_moves(turn)

        if not self.is_legal(move):
            return 0

        if move in legal:
            self.cells[toX][toY].set_piece(self.cells[fromX][fromY].piece)
            self.cells[fromX][fromY].set_piece(Piece.EMPTY)
            self.update_checked(not turn)
            return 1

        else:
            return 0

    def update_checked(self, turn):
        for i in range(8):
            for j in range(8):
                self.cells[i][j].white_checked = False
                self.cells[i][j].black_checked = False

        for i in range(8):
            for j in range(8):
                if self.cells[i][j].piece == Piece.WHITEPAWN:
                    if i > 0 and j < 7:
                        self.cells[i - 1][j + 1].white_checked = True
                    if i > 0 and j > 0:
                        self.cells[i - 1][j - 1].white_checked = True
                if self.cells[i][j].piece == Piece.BLACKPAWN:
                    if i < 7 and j < 7:
                        self.cells[i + 1][j + 1].black_checked = True
                    if i < 7 and j > 0:
                        self.cells[i + 1][j - 1].black_checked = True
                elif self.cells[i][j].piece == Piece.WHITEKNIGHT:
                    if i + 2 <= 7 and j + 1 <= 7:
                        self.cells[i + 2][j + 1].white_checked = True
                    if i + 2 <= 7 and j - 1 >= 0:
                        self.cells[i + 2][j - 1].white_checked = True
                    if i - 2 >= 0 and j + 1 <= 7:
                        self.cells[i - 2][j + 1].white_checked = True
                    if i - 2 >= 0 and j - 1 >= 0:
                        self.cells[i - 2][j - 1].white_checked = True
                    if j + 2 <= 7 and i + 1 <= 7:
                        self.cells[i + 1][j + 2].white_checked = True
                    if j + 2 <= 7 and i - 1 >= 0:
                        self.cells[i - 1][j + 2].white_checked = True
                    if j - 2 >= 0 and i + 1 <= 7:
                        self.cells[i + 1][j - 2].white_checked = True
                    if j - 2 >= 0 and i - 1 >= 0:
                        self.cells[i - 1][j - 2].white_checked = True
                elif self.cells[i][j].piece == Piece.BLACKKNIGHT:
                    if i + 2 <= 7 and j + 1 <= 7:
                        self.cells[i + 2][j + 1].black_checked = True
                    if i + 2 <= 7 and j - 1 >= 0:
                        self.cells[i + 2][j - 1].black_checked = True
                    if i - 2 >= 0 and j + 1 <= 7:
                        self.cells[i - 2][j + 1].black_checked = True
                    if i - 2 >= 0 and j - 1 >= 0:
                        self.cells[i - 2][j - 1].black_checked = True
                    if j + 2 <= 7 and i + 1 <= 7:
                        self.cells[i + 1][j + 2].black_checked = True
                    if j + 2 <= 7 and i - 1 >= 0:
                        self.cells[i - 1][j + 2].black_checked = True
                    if j - 2 >= 0 and i + 1 <= 7:
                        self.cells[i + 1][j - 2].black_checked = True
                    if j - 2 >= 0 and i - 1 >= 0:
                        self.cells[i - 1][j - 2].black_checked = True
                elif self.cells[i][j].piece == Piece.WHITEROOK:
                    for i1 in range(i + 1, 8):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i][j].white_checked = True
                            break
                        else:
                            self.cells[i][j].white_checked = True
                    for i1 in reversed(range(0, i)):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i][j].white_checked = True
                            break
                        else:
                            self.cells[i][j].white_checked = True
                    for j1 in range(j + 1, 8):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].white_checked = True
                            break
                        else:
                            self.cells[i][j1].white_checked = True
                    for j1 in reversed(range(0, j)):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].white_checked = True
                            break
                        else:
                            self.cells[i][j1].white_checked = True

    def is_legal(self, move):
        fromX = move[0]
        fromY = move[1]
        toX = move[2]
        toY = move[3]

        if self.cells[fromX][fromY].piece == Piece.EMPTY:
            return False

        if self.cells[fromX][fromY].color == self.cells[toX][toY].color:
            return False

        return True

    def generate_moves(self, turn):
        legal_moves = []

        if turn:
            for i in range(8):
                for j in range(8):
                    if self.cells[i][j].piece == Piece.WHITEPAWN:
                        if i > 0 and self.cells[i - 1][j].piece == Piece.EMPTY:
                            legal_moves.append((i, j, i - 1, j))
                        if i == 6 and self.cells[i - 2][j].piece == Piece.EMPTY and self.cells[i - 1][
                            j].piece == Piece.EMPTY:
                            legal_moves.append((i, j, i - 2, j))
                        if i > 0 and j < 7 and self.cells[i - 1][j + 1].color == 'black':
                            legal_moves.append((i, j, i - 1, j + 1))
                        if i > 0 and j > 0 and self.cells[i - 1][j - 1].color == 'black':
                            legal_moves.append((i, j, i - 1, j - 1))
                    elif self.cells[i][j].piece == Piece.WHITEKNIGHT:
                        if i + 2 <= 7 and j + 1 <= 7 and self.cells[i + 2][j + 1].color != 'white':
                            legal_moves.append((i, j, i + 2, j + 1))
                        if i + 2 <= 7 and j - 1 >= 0 and self.cells[i + 2][j - 1].color != 'white':
                            legal_moves.append((i, j, i + 2, j - 1))
                        if i - 2 >= 0 and j + 1 <= 7 and self.cells[i - 2][j + 1].color != 'white':
                            legal_moves.append((i, j, i - 2, j + 1))
                        if i - 2 >= 0 and j - 1 >= 0 and self.cells[i - 2][j - 1].color != 'white':
                            legal_moves.append((i, j, i - 2, j - 1))
                        if j + 2 <= 7 and i + 1 <= 7 and self.cells[i + 1][j + 2].color != 'white':
                            legal_moves.append((i, j, i + 1, j + 2))
                        if j + 2 <= 7 and i - 1 >= 0 and self.cells[i - 1][j + 2].color != 'white':
                            legal_moves.append((i, j, i - 1, j + 2))
                        if j - 2 >= 0 and i + 1 <= 7 and self.cells[i + 1][j - 2].color != 'white':
                            legal_moves.append((i, j, i + 1, j - 2))
                        if j - 2 >= 0 and i - 1 >= 0 and self.cells[i - 1][j - 2].color != 'white':
                            legal_moves.append((i, j, i - 1, j - 2))
                    elif self.cells[i][j].piece == Piece.WHITEROOK:
                        for i1 in range(i + 1, 8):
                            if self.cells[i1][j].color == 'white':
                                break
                            elif self.cells[i1][j].color == 'black':
                                legal_moves.append((i, j, i1, j))
                                break
                            else:
                                legal_moves.append((i, j, i1, j))
                        for i1 in reversed(range(0, i)):
                            if self.cells[i1][j].color == 'white':
                                break
                            elif self.cells[i1][j].color == 'black':
                                legal_moves.append((i, j, i1, j))
                                break
                            else:
                                legal_moves.append((i, j, i1, j))
                        for j1 in range(j + 1, 8):
                            if self.cells[i][j1].color == 'white':
                                break
                            elif self.cells[i][j1].color == 'black':
                                legal_moves.append((i, j, i, j1))
                                break
                            else:
                                legal_moves.append((i, j, i, j1))
                        for j1 in reversed(range(0, j)):
                            if self.cells[i][j1].color == 'white':
                                break
                            elif self.cells[i][j1].color == 'black':
                                legal_moves.append((i, j, i, j1))
                                break
                            else:
                                legal_moves.append((i, j, i, j1))
                    elif self.cells[i][j].piece == Piece.WHITEBISHOP:
                        for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                            if self.cells[i1][j1].color == 'white':
                                break
                            elif self.cells[i1][j1].color == 'black':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                            if self.cells[i1][j1].color == 'white':
                                break
                            elif self.cells[i1][j1].color == 'black':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                            if self.cells[i1][j1].color == 'white':
                                break
                            elif self.cells[i1][j1].color == 'black':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                            if self.cells[i1][j1].color == 'white':
                                break
                            elif self.cells[i1][j1].color == 'black':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))

        else:
            for i in range(8):
                for j in range(8):
                    if self.cells[i][j].piece == Piece.BLACKPAWN:
                        if i < 7 and self.cells[i + 1][j].piece == Piece.EMPTY:
                            legal_moves.append((i, j, i + 1, j))
                        if i == 1 and self.cells[i + 2][j].piece == Piece.EMPTY and self.cells[i + 1][
                            j].piece == Piece.EMPTY:
                            legal_moves.append((i, j, i + 2, j))
                        if i < 7 and j < 7 and self.cells[i + 1][j + 1].color == 'white':
                            legal_moves.append((i, j, i + 1, j + 1))
                        if i < 7 and j > 0 and self.cells[i + 1][j - 1].color == 'white':
                            legal_moves.append((i, j, i + 1, j - 1))
                    elif self.cells[i][j].piece == Piece.BLACKKNIGHT:
                        if i + 2 <= 7 and j + 1 <= 7 and self.cells[i + 2][j + 1].color != 'black':
                            legal_moves.append((i, j, i + 2, j + 1))
                        if i + 2 <= 7 and j - 1 >= 0 and self.cells[i + 2][j - 1].color != 'black':
                            legal_moves.append((i, j, i + 2, j - 1))
                        if i - 2 >= 0 and j + 1 <= 7 and self.cells[i - 2][j + 1].color != 'black':
                            legal_moves.append((i, j, i - 2, j + 1))
                        if i - 2 >= 0 and j - 1 >= 0 and self.cells[i - 2][j - 1].color != 'black':
                            legal_moves.append((i, j, i - 2, j - 1))
                        if j + 2 <= 7 and i + 1 <= 7 and self.cells[i + 1][j + 2].color != 'black':
                            legal_moves.append((i, j, i + 1, j + 2))
                        if j + 2 <= 7 and i - 1 >= 0 and self.cells[i - 1][j + 2].color != 'black':
                            legal_moves.append((i, j, i - 1, j + 2))
                        if j - 2 >= 0 and i + 1 <= 7 and self.cells[i + 1][j - 2].color != 'black':
                            legal_moves.append((i, j, i + 1, j - 2))
                        if j - 2 >= 0 and i - 1 >= 0 and self.cells[i - 1][j - 2].color != 'black':
                            legal_moves.append((i, j, i - 1, j - 2))
                    elif self.cells[i][j].piece == Piece.BLACKROOK:
                        for i1 in range(i + 1, 8):
                            if self.cells[i1][j].color == 'black':
                                break
                            elif self.cells[i1][j].color == 'white':
                                legal_moves.append((i, j, i1, j))
                                break
                            else:
                                legal_moves.append((i, j, i1, j))
                        for i1 in reversed(range(0, i)):
                            if self.cells[i1][j].color == 'black':
                                break
                            elif self.cells[i1][j].color == 'white':
                                legal_moves.append((i, j, i1, j))
                                break
                            else:
                                legal_moves.append((i, j, i1, j))
                        for j1 in range(j + 1, 8):
                            if self.cells[i][j1].color == 'black':
                                break
                            elif self.cells[i][j1].color == 'white':
                                legal_moves.append((i, j, i, j1))
                                break
                            else:
                                legal_moves.append((i, j, i, j1))
                        for j1 in reversed(range(0, j)):
                            if self.cells[i][j1].color == 'black':
                                break
                            elif self.cells[i][j1].color == 'white':
                                legal_moves.append((i, j, i, j1))
                                break
                            else:
                                legal_moves.append((i, j, i, j1))
                    elif self.cells[i][j].piece == Piece.BLACKBISHOP:
                        for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                            if self.cells[i1][j1].color == 'black':
                                break
                            elif self.cells[i1][j1].color == 'white':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                            if self.cells[i1][j1].color == 'black':
                                break
                            elif self.cells[i1][j1].color == 'white':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                            if self.cells[i1][j1].color == 'black':
                                break
                            elif self.cells[i1][j1].color == 'white':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))
                        for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                            if self.cells[i1][j1].color == 'black':
                                break
                            elif self.cells[i1][j1].color == 'white':
                                legal_moves.append((i, j, i1, j1))
                                break
                            else:
                                legal_moves.append((i, j, i1, j1))

        return legal_moves
