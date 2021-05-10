from enum import Enum


class Piece(Enum):
    WHITEPAWN = 'pawn'
    BLACKPAWN = 'Bpawn'
    WHITEROOK = 'rook'
    BLACKROOK = 'Brook'
    WHITEBISHOP = 'bishop'
    BLACKBISHOP = 'Bbishop'
    WHITEKNIGHT = 'knight'
    BLACKKNIGHT = 'Bknight'
    WHITEQUEEN = 'queen'
    BLACKQUEEN = 'Bqueen'
    WHITEKING = 'king'
    BLACKKING = 'Bking'
    EMPTY = '#'
