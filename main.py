import discord
from discord.ext import commands
import board_generator as bg
import Board

client = commands.Bot(command_prefix='~')

board = Board.Board()

white = None
black = None

turn = True


@client.event
async def on_ready():
    print('ready')
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Chess'))


@client.command()
async def show_board(ctx):
    bg.generate_board(board)
    await ctx.channel.send(file=discord.File('chessboard.png'))


@client.command()
async def move(ctx, move: str):
    global board
    global turn

    # if white is None and black is None:
    #     await ctx.channel.send('No game is currently running')
    #     return
    #
    # elif ctx.message.author != white and ctx.message.author != black:
    #     await ctx.channel.send('You are not a player in this game')
    #     return
    #
    # elif (ctx.message.author == white and turn == False) or (ctx.message.author == black and turn == True):
    #     await ctx.channel.send('It is not your turn')
    #     return

    letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    numbers = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    move = move.lower()
    if len(move) != 4:
        await ctx.channel.send('Invalid move')
        return
    moveFrom = move[:2]
    moveTo = move[2:]

    if moveFrom[0] not in letters or moveTo[0] not in letters or moveFrom[1] not in numbers or moveTo[1] not in numbers:
        await ctx.channel.send('Invalid move')

    if board.move((numbers[moveFrom[1]], letters[moveFrom[0]], numbers[moveTo[1]], letters[moveTo[0]]), turn) == 1:
        turn = not turn
        await show_board(ctx)

    else:
        await ctx.channel.send('Invalid move')


@client.command()
async def reset(ctx):
    global board
    global turn
    board = Board.Board()
    turn = True


@client.command()
async def start(ctx, opponent: discord.Member):
    global black, white

    white = ctx.message.author
    black = opponent

    if white == black:
        await ctx.channel.send('You can\'t play against yourself')
        black = None
        white = None
    else:
        await ctx.channel.send(f'{white.mention} and {black.mention} are playing')
        await show_board(ctx)


@client.command()
async def end(ctx):
    global board

    if black is None or white is None:
        await ctx.channel.send('No game is currently running')

    elif ctx.message.author == black or ctx.message.author == white:
        await ctx.channel.send(f'The game between {white.mention} and {black.mention} has ended')
        await reset(ctx)

    else:
        await ctx.channel.send('Only the players can end the game')


client.run('ODQwMjc5MDUxNTI3NjUxMzQ5.YJV42Q.hllVtsxQT7u0jR0SSwPD5Qz7D6Y')
