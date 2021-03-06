from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import PIL.ImageOps

from Board import Board
from Piece import Piece


def generate_board(board):
    w, h = 9, 9
    img = Image.new("RGB", (w, h))
    img_flipped = Image.new("RGB", (w, h))
    pixels = img.load()
    pixels_flipped = img_flipped.load()

    for i in range(w):
        for j in range(h):
            pixels[i, j] = (54, 57, 63)
            pixels_flipped[i, j] = (54, 57, 63)

    for i in range(1, 9):
        for j in range(8):
            if not (i + j) % 2:
                pixels[i, j] = (204, 114, 49)
                pixels_flipped[i, j] = (204, 114, 49)
            else:
                pixels[i, j] = (252, 182, 131)
                pixels_flipped[i, j] = (252, 182, 131)

    img = img.resize((900, 900), Image.NEAREST)
    img_flipped = img_flipped.resize((900, 900), Image.NEAREST)
    draw = ImageDraw.Draw(img)
    draw_flipped = ImageDraw.Draw(img_flipped)
    font = ImageFont.truetype('C:\\windows\\fonts\\arial.ttf', 72)
    for i in range(8):
        draw.text((25, (100 * i) + 10), f"{8 - i}", (153, 170, 181), font=font)
        draw_flipped.text((25, (100 * i) + 10), f"{i + 1}", (153, 170, 181), font=font)
        draw.text(((100 * (i + 1)) + 25, 810),
                  f"{'A' if i == 0 else 'B' if i == 1 else 'C' if i == 2 else 'D' if i == 3 else 'E' if i == 4 else 'F' if i == 5 else 'G' if i == 6 else 'H'}",
                  (153, 170, 181), font=font)
        draw_flipped.text(((100 * (i + 1)) + 25, 810),
                  f"{'A' if i == 7 else 'B' if i == 6 else 'C' if i == 5 else 'D' if i == 4 else 'E' if i == 3 else 'F' if i == 2 else 'G' if i == 1 else 'H'}",
                  (153, 170, 181), font=font)

    set_board(board, img, img_flipped)


def set_board(board, board_image, board_image_flipped):
    for i in range(8):
        for j in range(8):
            if not board.cells[i][j].piece == Piece.EMPTY:
                piece = Image.open(f'pieces/{board.cells[i][j].piece.value}.png')
                piece = piece.resize((100, 100), Image.NEAREST)
                board_image.paste(piece, cell_at((i, j)), mask=piece)
            else:
                clear_cell(board_image, (i, j))

            if not board.cells[i][j].piece == Piece.EMPTY:
                piece_flipped = Image.open(f'pieces/{board.cells[i][j].piece.value}.png')
                piece_flipped = piece_flipped.resize((100, 100), Image.NEAREST)
                board_image_flipped.paste(piece_flipped, cell_at((abs(i-7), abs(j-7))), mask=piece_flipped)
            else:
                clear_cell(board_image_flipped, (abs(i-7), abs(j-7)))

    board_image.save('chessboard.png')
    board_image_flipped.save('chessboard_flipped.png')


def cell_at(position):
    return (position[1] + 1) * 100, position[0] * 100


def invert_piece(piece):
    image = Image.open(f'pieces/{piece}.png')
    r, g, b, a = image.split()
    rgb_image = Image.merge('RGB', (r, g, b))

    inverted_image = PIL.ImageOps.invert(rgb_image)

    r2, g2, b2 = inverted_image.split()

    final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

    return final_transparent_image


def clear_cell(board, position):
    color = (204, 114, 49) if (position[0] + position[1]) % 2 else (252, 182, 131)
    img = Image.new("RGB", (100, 100), color)
    board.paste(img, cell_at(position))
    return board
