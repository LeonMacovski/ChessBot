import discord
from discord.abc import Messageable
from discord.ext import commands
import board_generator as bg
import Board

client = commands.Bot(command_prefix='~')

board = Board.Board()

white = None
black = None

turn = True

last_image = None


@client.event
async def on_ready():
    print('ready')
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Chess'))


@client.command()
async def show_board(ctx):
    '''
    Prints the current board to the channel if there is a game running
    :param ctx:
    :return:
    '''
    global last_image
    if white is None and black is None:
        await ctx.channel.send('No game is currently running')
        return
    bg.generate_board(board)

    if turn:
        await ctx.channel.send(file=discord.File('chessboard.png'))
    else:
        await ctx.channel.send(file=discord.File('chessboard_flipped.png'))

    if last_image is not None:
        await last_image.delete()

    async for x in Messageable.history(ctx.message.channel, limit=1):
        last_image = x


@client.command()
async def move(ctx, move: str):
    '''
    Moves a piece. The move sintax is <letter><number><letter><number> ex. a2a4 to move the piece on a2 to a4
    :param ctx:
    :param move:
    :return:
    '''
    global board
    global turn

    if white is None and black is None:
        await ctx.channel.send('No game is currently running')
        return

    elif ctx.message.author != white and ctx.message.author != black:
        await ctx.channel.send('You are not a player in this game')
        return

    elif (ctx.message.author == white and turn == False) or (ctx.message.author == black and turn == True):
        await ctx.channel.send('It is not your turn')
        return

    if board.move(move, turn) == 1:
        turn = not turn
        await show_board(ctx)
        if board.winner == 'white':
            await ctx.channel.send(f"{white.mention} has won!")
            await end(ctx)
        elif board.winner == 'black':
            await ctx.channel.send(f"{black.mention} has won!")
            await end(ctx)

    else:
        await ctx.channel.send('Invalid move')


@client.command()
async def reset(ctx):
    '''
    Resets the board position. Can only be done by the players of the game
    :param ctx:
    :return:
    '''
    if white is None and black is None:
        await ctx.channel.send('No game is currently running')
        return
    if ctx.message.author != white and ctx.message.author != black:
        await ctx.channel.send('You are not a player in this game')
        return
    global board
    global turn
    board = Board.Board()
    turn = True
    await show_board(ctx)


@client.command()
async def start(ctx, opponent: discord.Member):
    '''
    Starts a game with yourself and the person you tagged. The person who started the game is white
    :param ctx:
    :param opponent:
    :return:
    '''
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
    '''
    Ends the game if there is one
    :param ctx:
    :return:
    '''
    global board

    if black is None or white is None:
        await ctx.channel.send('No game is currently running')

    elif ctx.message.author == black or ctx.message.author == white:
        await ctx.channel.send(f'The game between {white.mention} and {black.mention} has ended')
        await reset(ctx)

    else:
        await ctx.channel.send('Only the players can end the game')


token = '' #enter your bot token
client.run(token)

