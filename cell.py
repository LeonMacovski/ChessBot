from Piece import Piece

class Cell:
    def __init__(self, pos, piece=Piece.EMPTY):
        self.piece = piece
        self.pos = pos
        self.white_checked = False
        self.black_checked = False
        self.color = None

    def set_piece(self, piece):
        self.piece = piece
        self.color = None if piece.value == '#' else 'black' if piece.value.startswith('B') else 'white'
