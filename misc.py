from turtle import title
import discord
from discord.ext import commands
import random
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

from bot import *
class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    

    @client.command()
    async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send("Oyun zaten devam ediyor.")

    @client.command()
    async def place(ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    Misc.checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Lutfen 1 ile 9 arasinda bir sayi secin ve sececeginiz sayi bos bir kareye denk gelsin.")
            else:
                await ctx.send('Sira sende degil.')
        else:
            await ctx.send("Yeni bir oyun baslatin lutfen.")
    def checkWinner(winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Iki kisiyi taglemeniz lazim oyun icin.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Kendini ve oyunu oynamak istediginiz kisiyi tagleyin. Or: @Danteh")

    @place.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Tahtadaki sayilar soldan saga 1 ile 9 arasinda numaralandirilmistir. ")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Lutfen bir sayi giriniz.")
def setup(bot):
    bot.add_cog(Misc(bot))