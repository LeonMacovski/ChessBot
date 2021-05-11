from Piece import Piece
from cell import Cell


class Board:
    def __init__(self):
        self.black_en_passant_file = None
        self.white_en_passant_file = None
        self.winner = None
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_h_rook_moved = False
        self.white_a_rook_moved = False
        self.black_h_rook_moved = False
        self.black_a_rook_moved = False
        self.cells = []
        self.state = [['Brook', 'Bknight', 'Bbishop', 'Bqueen', 'Bking', 'Bbishop', 'Bknight', 'Brook'],
                      ['Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn', 'Bpawn'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['#', '#', '#', '#', '#', '#', '#', '#'],
                      ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'],
                      ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']]

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
        move = move.lower()
        if move == '0-0':
            if turn:
                if self.white_king_moved or self.white_h_rook_moved:
                    return 0
                if self.cells[7][7].piece != Piece.WHITEROOK:
                    return 0
                if self.cells[7][4].piece != Piece.WHITEKING:
                    return 0
                if self.cells[7][5].piece != Piece.EMPTY or self.cells[7][6].piece != Piece.EMPTY:
                    return 0
                if self.cells[7][4].black_checked or self.cells[7][5].black_checked or self.cells[7][6].black_checked:
                    return 0
                self.cells[7][4].piece = Piece.EMPTY
                self.cells[7][5].piece = Piece.WHITEROOK
                self.cells[7][6].piece = Piece.WHITEKING
                self.cells[7][7].piece = Piece.EMPTY
                self.white_king_moved = True
                self.white_h_rook_moved = True
                return 1

            else:
                if self.black_king_moved or self.black_h_rook_moved:
                    return 0
                if self.cells[0][7].piece != Piece.BLACKROOK:
                    return 0
                if self.cells[0][4].piece != Piece.BLACKKING:
                    return 0
                if self.cells[0][5].piece != Piece.EMPTY or self.cells[0][6].piece != Piece.EMPTY:
                    return 0
                if self.cells[0][4].white_checked or self.cells[0][5].white_checked or self.cells[0][6].white_checked:
                    return 0
                self.cells[0][4].piece = Piece.EMPTY
                self.cells[0][5].piece = Piece.BLACKROOK
                self.cells[0][6].piece = Piece.BLACKKING
                self.cells[0][7].piece = Piece.EMPTY
                self.black_king_moved = True
                self.black_h_rook_moved = True
                return 1

        if move == '0-0-0':
            if turn:
                if self.white_king_moved or self.white_a_rook_moved:
                    return 0
                if self.cells[7][0].piece != Piece.WHITEROOK:
                    return 0
                if self.cells[7][4].piece != Piece.WHITEKING:
                    return 0
                if self.cells[7][1].piece != Piece.EMPTY or self.cells[7][2].piece != Piece.EMPTY or self.cells[7][
                    3].piece != Piece.EMPTY:
                    return 0
                if self.cells[7][1].black_checked or self.cells[7][2].black_checked or self.cells[7][3].black_checked or \
                        self.cells[7][4].black_checked:
                    return 0
                self.cells[7][0].piece = Piece.EMPTY
                self.cells[7][2].piece = Piece.WHITEKING
                self.cells[7][3].piece = Piece.WHITEROOK
                self.cells[7][4].piece = Piece.EMPTY
                self.white_king_moved = True
                self.white_a_rook_moved = True
                return 1

            else:
                if self.black_king_moved or self.black_a_rook_moved:
                    return 0
                if self.cells[0][0].piece != Piece.BLACKROOK:
                    return 0
                if self.cells[0][4].piece != Piece.BLACKKING:
                    return 0
                if self.cells[0][1].piece != Piece.EMPTY or self.cells[0][2].piece != Piece.EMPTY or self.cells[0][
                    3].piece != Piece.EMPTY:
                    return 0
                if self.cells[0][1].white_checked or self.cells[0][2].white_checked or self.cells[0][3].white_checked or \
                        self.cells[0][4].white_checked:
                    return 0
                self.cells[7][0].piece = Piece.EMPTY
                self.cells[7][2].piece = Piece.BLACKKING
                self.cells[7][3].piece = Piece.BLACKROOK
                self.cells[7][4].piece = Piece.EMPTY
                self.black_king_moved = True
                self.black_a_rook_moved = True
                return 1

        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        numbers = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        if len(move) != 4:
            return 0
        moveFrom = move[:2]
        moveTo = move[2:]
        if moveFrom[0] not in letters or moveTo[0] not in letters or moveFrom[1] not in numbers or moveTo[
            1] not in numbers:
            return 0

        fromY = letters[moveFrom[0]]
        fromX = numbers[moveFrom[1]]
        toY = letters[moveTo[0]]
        toX = numbers[moveTo[1]]

        move = (numbers[moveFrom[1]], letters[moveFrom[0]], numbers[moveTo[1]], letters[moveTo[0]])

        if not self.is_legal(move):
            return 0

        legal = self.generate_moves(turn)

        if move in legal:
            fromPiece = self.cells[fromX][fromY].piece
            toPiece = self.cells[toX][toY].piece
            self.cells[toX][toY].set_piece(fromPiece)
            self.cells[fromX][fromY].set_piece(Piece.EMPTY)
            self.update_checked()

            if fromPiece == Piece.WHITEKING:
                self.white_king_moved = True
            if fromPiece == Piece.BLACKKING:
                self.black_king_moved = True
            if fromX == 7 and fromY == 0:
                self.white_a_rook_moved = True
            if fromX == 0 and fromY == 0:
                self.black_a_rook_moved = True
            if fromX == 7 and fromY == 7:
                self.white_h_rook_moved = True
            if fromX == 0 and fromY == 7:
                self.black_h_rook_moved = True

            white_flag = True
            black_flag = True

            if fromPiece == Piece.WHITEPAWN and fromX == 6 and toX == 4:
                self.white_en_passant_file = fromY
                white_flag = False

            if fromPiece == Piece.BLACKPAWN and fromX == 1 and toX == 3:
                self.black_en_passant_file = fromY
                black_flag = False

            if white_flag:
                self.white_en_passant_file = None
            if black_flag:
                self.black_en_passant_file = None

            if fromPiece == Piece.WHITEPAWN and fromY != toY and toPiece == Piece.EMPTY:
                self.cells[toX + 1][toY].set_piece(Piece.EMPTY)
                self.black_en_passant_file = None

            if fromPiece == Piece.BLACKPAWN and fromY != toY and toPiece == Piece.EMPTY:
                self.cells[toX - 1][toY].set_piece(Piece.EMPTY)
                self.white_en_passant_file = None

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
                        if i == 3 and j > 0 and self.cells[i][
                            j - 1].piece == Piece.BLACKPAWN and self.black_en_passant_file == j - 1:
                            legal_moves.append((i, j, i - 1, j - 1))
                        if i == 3 and j < 7 and self.cells[i][
                            j + 1].piece == Piece.BLACKPAWN and self.black_en_passant_file == j + 1:
                            legal_moves.append((i, j, i - 1, j + 1))



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
                        if i > 0 and self.cells[i - 1][j].color != 'white':
                            legal_moves.append((i, j, i - 1, j))
                        if i < 7 and self.cells[i + 1][j].color != 'white':
                            legal_moves.append((i, j, i + 1, j))
                        if j > 0 and self.cells[i][j - 1].color != 'white':
                            legal_moves.append((i, j, i, j - 1))
                        if j < 7 and self.cells[i][j + 1].color != 'white':
                            legal_moves.append((i, j, i, j + 1))
                        if i > 0 and j > 0 and self.cells[i - 1][j - 1].color != 'white':
                            legal_moves.append((i, j, i - 1, j - 1))
                        if i > 0 and j < 7 and self.cells[i - 1][j + 1].color != 'white':
                            legal_moves.append((i, j, i - 1, j + 1))
                        if i < 7 and j > 0 and self.cells[i + 1][j - 1].color != 'white':
                            legal_moves.append((i, j, i + 1, j - 1))
                        if i < 7 and j < 7 and self.cells[i + 1][j + 1].color != 'white':
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
                        if i == 4 and j > 0 and self.cells[i][
                            j - 1].piece == Piece.WHITEPAWN and self.white_en_passant_file == j - 1:
                            legal_moves.append((i, j, i + 1, j - 1))
                        if i == 4 and j < 7 and self.cells[i][
                            j + 1].piece == Piece.WHITEPAWN and self.white_en_passant_file == j + 1:
                            legal_moves.append((i, j, i + 1, j + 1))
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
                        if i > 0 and self.cells[i - 1][j].color != 'black':
                            legal_moves.append((i, j, i - 1, j))
                        if i < 7 and self.cells[i + 1][j].color != 'black':
                            legal_moves.append((i, j, i + 1, j))
                        if j > 0 and self.cells[i][j - 1].color != 'black':
                            legal_moves.append((i, j, i, j - 1))
                        if j < 7 and self.cells[i][j + 1].color != 'black':
                            legal_moves.append((i, j, i, j + 1))
                        if i > 0 and j > 0 and self.cells[i - 1][j - 1].color != 'black':
                            legal_moves.append((i, j, i - 1, j - 1))
                        if i > 0 and j < 7 and self.cells[i - 1][j + 1].color != 'black':
                            legal_moves.append((i, j, i - 1, j + 1))
                        if i < 7 and j > 0 and self.cells[i + 1][j - 1].color != 'black':
                            legal_moves.append((i, j, i + 1, j - 1))
                        if i < 7 and j < 7 and self.cells[i + 1][j + 1].color != 'black':
                            legal_moves.append((i, j, i + 1, j + 1))

        return self.filter_moves(turn, legal_moves)
