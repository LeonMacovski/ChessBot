from Piece import Piece
from cell import Cell


class Board:
    def __init__(self):
        self.winner = None
        self.cells = []
        self.state = [['Brook', 'Bknight', 'Bbishop', 'Bqueen', 'Bking', 'Bbishop', 'Bknight', 'Brook'],
                      ['Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'],
                      ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']]

        # self.state = [['#', '#', '#', '#', 'king', '#', '#', '#'],
        #               ['Bqueen', 'Brook', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#'],
        #               ['#', '#', '#', '#', '#', '#', '#', '#']]

        for i in range(8):
            row = []
            for j in range(8):
                row.append(Cell((i, j)))
                row[j].set_piece(Piece(self.state[i][j]))
            self.cells.append(row)

        self.update_checked()

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

        if not self.is_legal(move):
            return 0

        legal = self.generate_moves(turn)

        if move in legal:
            fromPiece = self.cells[fromX][fromY].piece
            toPiece = self.cells[toX][toY].piece
            self.cells[toX][toY].set_piece(fromPiece)
            self.cells[fromX][fromY].set_piece(Piece.EMPTY)
            self.update_checked()
            temp = self.generate_moves(not turn)
            if len(temp) == 0:
                self.winner = f'{"white" if turn else "black"}'

            return 1

        else:
            return 0

    def filter_moves(self, turn, moves):
        new_moves = []
        for move in moves:
            fromX = move[0]
            fromY = move[1]
            toX = move[2]
            toY = move[3]

            fromPiece = self.cells[fromX][fromY].piece
            toPiece = self.cells[toX][toY].piece
            self.cells[toX][toY].set_piece(fromPiece)
            self.cells[fromX][fromY].set_piece(Piece.EMPTY)
            self.update_checked()

            should_include = True

            for i in range(8):
                for j in range(8):
                    if turn and self.cells[i][j].piece == Piece.WHITEKING and self.cells[i][j].black_checked:
                        self.cells[fromX][fromY].set_piece(fromPiece)
                        self.cells[toX][toY].set_piece(toPiece)
                        self.update_checked()
                        should_include = False
                        break
                    if not turn and self.cells[i][j].piece == Piece.BLACKKING and self.cells[i][j].white_checked:
                        self.cells[fromX][fromY].set_piece(fromPiece)
                        self.cells[toX][toY].set_piece(toPiece)
                        self.update_checked()
                        should_include = False
                        break
                if not should_include:
                    break

            if should_include:
                self.cells[fromX][fromY].set_piece(fromPiece)
                self.cells[toX][toY].set_piece(toPiece)
                self.update_checked()
                new_moves.append(move)

        return new_moves

    def update_checked(self):
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
                elif self.cells[i][j].piece == Piece.BLACKPAWN:
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
                            self.cells[i1][j].white_checked = True
                            break
                        else:
                            self.cells[i1][j].white_checked = True
                    for i1 in reversed(range(0, i)):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].white_checked = True
                            break
                        else:
                            self.cells[i1][j].white_checked = True
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
                elif self.cells[i][j].piece == Piece.BLACKROOK:
                    for i1 in range(i + 1, 8):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].black_checked = True
                            break
                        else:
                            self.cells[i1][j].black_checked = True
                    for i1 in reversed(range(0, i)):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].black_checked = True
                            break
                        else:
                            self.cells[i1][j].black_checked = True
                    for j1 in range(j + 1, 8):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].black_checked = True
                            break
                        else:
                            self.cells[i][j1].black_checked = True
                    for j1 in reversed(range(0, j)):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].black_checked = True
                            break
                        else:
                            self.cells[i][j1].black_checked = True
                elif self.cells[i][j].piece == Piece.WHITEBISHOP:
                    for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                elif self.cells[i][j].piece == Piece.BLACKBISHOP:
                    for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                elif self.cells[i][j].piece == Piece.WHITEQUEEN:
                    for i1 in range(i + 1, 8):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].white_checked = True
                            break
                        else:
                            self.cells[i1][j].white_checked = True
                    for i1 in reversed(range(0, i)):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].white_checked = True
                            break
                        else:
                            self.cells[i1][j].white_checked = True
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
                    for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                    for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].white_checked = True
                            break
                        else:
                            self.cells[i1][j1].white_checked = True
                elif self.cells[i][j].piece == Piece.BLACKQUEEN:
                    for i1 in range(i + 1, 8):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].black_checked = True
                            break
                        else:
                            self.cells[i1][j].black_checked = True
                    for i1 in reversed(range(0, i)):
                        if self.cells[i1][j].piece != Piece.EMPTY:
                            self.cells[i1][j].black_checked = True
                            break
                        else:
                            self.cells[i1][j].black_checked = True
                    for j1 in range(j + 1, 8):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].black_checked = True
                            break
                        else:
                            self.cells[i][j1].black_checked = True
                    for j1 in reversed(range(0, j)):
                        if self.cells[i][j1].piece != Piece.EMPTY:
                            self.cells[i][j1].black_checked = True
                            break
                        else:
                            self.cells[i][j1].black_checked = True
                    for i1, j1 in zip(reversed(range(0, i)), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(reversed(range(0, i)), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(range(i + 1, 8), reversed(range(0, j))):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                    for i1, j1 in zip(range(i + 1, 8), range(j + 1, 8)):
                        if self.cells[i1][j1].piece != Piece.EMPTY:
                            self.cells[i1][j1].black_checked = True
                            break
                        else:
                            self.cells[i1][j1].black_checked = True
                elif self.cells[i][j].piece == Piece.WHITEKING:
                    if i > 0:
                        self.cells[i - 1][j].white_checked = True
                    if i < 7:
                        self.cells[i + 1][j].white_checked = True
                    if j > 0:
                        self.cells[i][j - 1].white_checked = True
                    if j < 7:
                        self.cells[i][j + 1].white_checked = True
                    if i > 0 and j > 0:
                        self.cells[i - 1][j - 1].white_checked = True
                    if i > 0 and j < 7:
                        self.cells[i - 1][j + 1].white_checked = True
                    if i < 7 and j > 0:
                        self.cells[i + 1][j - 1].white_checked = True
                    if i < 7 and j < 7:
                        self.cells[i + 1][j + 1].white_checked = True
                elif self.cells[i][j].piece == Piece.BLACKKING:
                    if i > 0:
                        self.cells[i - 1][j].black_checked = True
                    if i < 7:
                        self.cells[i + 1][j].black_checked = True
                    if j > 0:
                        self.cells[i][j - 1].black_checked = True
                    if j < 7:
                        self.cells[i][j + 1].black_checked = True
                    if i > 0 and j > 0:
                        self.cells[i - 1][j - 1].black_checked = True
                    if i > 0 and j < 7:
                        self.cells[i - 1][j + 1].black_checked = True
                    if i < 7 and j > 0:
                        self.cells[i + 1][j - 1].black_checked = True
                    if i < 7 and j < 7:
                        self.cells[i + 1][j + 1].black_checked = True

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
                    elif self.cells[i][j].piece == Piece.WHITEQUEEN:
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
                    elif self.cells[i][j].piece == Piece.WHITEKING:
                        if i > 0 and self.cells[i-1][j].color != 'white':
                            legal_moves.append((i, j, i - 1, j))
                        if i < 7 and self.cells[i+1][j].color != 'white':
                            legal_moves.append((i, j, i + 1, j))
                        if j > 0 and self.cells[i][j-1].color != 'white':
                            legal_moves.append((i, j, i, j - 1))
                        if j < 7 and self.cells[i][j+1].color != 'white':
                            legal_moves.append((i, j, i, j + 1))
                        if i > 0 and j > 0 and self.cells[i-1][j-1].color != 'white':
                            legal_moves.append((i, j, i - 1, j - 1))
                        if i > 0 and j < 7 and self.cells[i-1][j+1].color != 'white':
                            legal_moves.append((i, j, i - 1, j + 1))
                        if i < 7 and j > 0 and self.cells[i+1][j-1].color != 'white':
                            legal_moves.append((i, j, i + 1, j - 1))
                        if i < 7 and j < 7 and self.cells[i+1][j+1].color != 'white':
                            legal_moves.append((i, j, i + 1, j + 1))

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
                    elif self.cells[i][j].piece == Piece.BLACKQUEEN:
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
                    elif self.cells[i][j].piece == Piece.BLACKKING:
                        if i > 0 and self.cells[i-1][j].color != 'black':
                            legal_moves.append((i, j, i - 1, j))
                        if i < 7 and self.cells[i+1][j].color != 'black':
                            legal_moves.append((i, j, i + 1, j))
                        if j > 0 and self.cells[i][j-1].color != 'black':
                            legal_moves.append((i, j, i, j - 1))
                        if j < 7 and self.cells[i][j+1].color != 'black':
                            legal_moves.append((i, j, i, j + 1))
                        if i > 0 and j > 0 and self.cells[i-1][j-1].color != 'black':
                            legal_moves.append((i, j, i - 1, j - 1))
                        if i > 0 and j < 7 and self.cells[i-1][j+1].color != 'black':
                            legal_moves.append((i, j, i - 1, j + 1))
                        if i < 7 and j > 0 and self.cells[i+1][j-1].color != 'black':
                            legal_moves.append((i, j, i + 1, j - 1))
                        if i < 7 and j < 7 and self.cells[i+1][j+1].color != 'black':
                            legal_moves.append((i, j, i + 1, j + 1))

        return self.filter_moves(turn, legal_moves)
