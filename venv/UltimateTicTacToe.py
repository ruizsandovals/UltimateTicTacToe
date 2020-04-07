#
# Ultimate Tic Tac Toe Game
#
# Author : Sergio Ruiz Sandoval
# Date   : April 7th 2020
#
# Description:
#
#   The objective to this game variant is to win three in a row in the smaller grid inside the greatest grid
#
#   Example
#
#     X |   | X #   |   |   #   |   | O
#    ---+---+---#---+---+---#---+---+---
#       | O |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   | O #   |   |   # X |   | X
#    ###################################
#       |   |   # O |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   | O |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   # X | O | X #   |   |
#    ###################################
#     X |   |   #   |   |   # O | X | O
#    ---+---+---#---+---+---#---+---+---
#       |   | O #   | X |   #   | X |     <------------ X wins, three in a row in the smaller grid
#    ---+---+---#---+---+---#---+---+---
#     O |   | X #   | 0 | X # O | X | O
#
#    According to the rules of the ultimate tic tac toe, once a player places a "O" (or "X" in case of the computer)
#    the next grid to be played is determined by the previous player move
#
#
#       |   |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   |   |   #   |   |    <-------------X plays here
#    ---+---+---#---+---+---#---+---+---
#       |   | X #   |   |   #   |   |
#    ###################################
#       |   |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   |   |   #   |   |
#    ###################################
#       |   |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   |   |   #   |   |
#    ---+---+---#---+---+---#---+---+---
#       |   |   #   |   |   #   |   | O  <------------- then O must play here
#
#  Notes:
#
#       Computer uses minimax algorithm, however due to the number of possible plays and processor consumption...
#       analysis is limited by the maxDepth variable.
#
#       The interface shows the scores of the las possible moves available for the computer player
#
#       The mainBoard is represented by an unidimensional array of 81 characters
#
#       The solution is created with Python using TKInter as the user interface

# import only system from os
from os import system, name
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import time
import random

# Constants
WIN = +10
LOSE = -10
TIE = 0
UNKNOWN = -5
PLAYER_X = "X"
PLAYER_O = "O"
BLANK = " "


class TTTExt():

    # Constructor
    def __init__(self, root):
        # Instance variables
        self.mainBoard = [BLANK for i in range(0, 81)]
        self.winningLines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
        self.winnerLine = []
        self.totalMoves = 81
        self.currentMove = 1
        self.lastMove = -1
        self.computerPlayer = PLAYER_X
        self.humanPlayer = PLAYER_O
        self.currentPlayer = PLAYER_X
        self.gameStatus = UNKNOWN
        self.gameWinner = UNKNOWN
        self.scoreHP = 0
        self.scoreCP = 0
        self.scoreTIE = 0

        # Computer control variables
        self.iterations = 0
        self.progress = 0.0
        self.depthReached = 0
        self.maxDepth = 1
        self.bestScore = 0

        # Interface creation
        self.root = root
        root.title("Utltimate Tic Tac Toe")
        root.geometry("900x800")
        # root.resizable (0,0)

        # Gets the requested values of the height and widht.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth() / 2 - 1000 / 2)
        positionDown = int(root.winfo_screenheight() / 2 - 800 / 2)

        # Positions the window in the center of the page.
        root.geometry("+{}+{}".format(positionRight, positionDown))

        # MAIN WINDOWS
        self.panedWindow = ttk.PanedWindow(root, orient=HORIZONTAL)
        self.panedWindow.pack(fill=BOTH, expand=True)

        # FRAMES
        self.parentLeftFrame = ttk.Frame(self.panedWindow, width=250, height=600, relief=SUNKEN)
        self.parentRightFrame = ttk.Frame(self.panedWindow, width=530, height=600, relief=SUNKEN)
        self.panedWindow.add(self.parentLeftFrame, weight=1)
        self.panedWindow.add(self.parentRightFrame, weight=3)

        # Left frames
        self.upperLeftFrame = ttk.Frame(self.parentLeftFrame, width=150, height=120, relief=SUNKEN)
        self.bottomLeftFrame = ttk.Frame(self.parentLeftFrame, width=150, height=200, relief=SUNKEN)
        self.upperLeftFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.bottomLeftFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Right Frames
        self.upperRightFrame = ttk.Frame(self.parentRightFrame, width=530, height=120, relief=SUNKEN)
        self.middleRightFrame = ttk.Frame(self.parentRightFrame, width=530, height=200, relief=SUNKEN)
        self.bottomRightFrame = ttk.Frame(self.parentRightFrame, width=530, height=120, relief=SUNKEN)
        self.upperRightFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.middleRightFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.bottomRightFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # SCORES
        # Human Player
        self.lblHP = ttk.Label(self.upperRightFrame, text="Human     ->", anchor="w", width=18)
        self.lblHP.grid(row=1, column=0, padx=10, pady=25, sticky="nsew")
        self.lblHP.config(font=("Consolas", 14))

        self.lblScoreHP = ttk.Label(self.upperRightFrame, width=5, text="0", anchor="w")
        self.lblScoreHP.grid(row=1, column=1, padx=10, pady=25, sticky="nsew")
        self.lblScoreHP.config(font=("Consolas", 14, "bold"), foreground="blue")
        self.lblScoreHP['text'] = str(self.scoreHP)

        # Computer Player
        self.lblCP = ttk.Label(self.upperRightFrame, text="<- Computer ", anchor="e", width=18)
        self.lblCP.grid(row=1, column=4, padx=10, pady=25, sticky="nsew")
        self.lblCP.config(font=("Consolas", 14))

        self.lblScoreCP = ttk.Label(self.upperRightFrame, width=5, text="0", anchor="e")
        self.lblScoreCP.grid(row=1, column=3, padx=10, pady=25, sticky="nsew")
        self.lblScoreCP.config(font=("Consolas", 14, "bold"), foreground="blue")
        self.lblScoreCP['text'] = str(self.scoreCP)

        # Draws
        self.lblTIE = ttk.Label(self.upperRightFrame, text="Draws", width=5, anchor="center")
        self.lblTIE.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        self.lblTIE.config(font=("Consolas", 14))

        self.lblScoreTIE = ttk.Label(self.upperRightFrame, width=5, text="0", anchor="center")
        self.lblScoreTIE.grid(row=1, column=2, padx=10, pady=25, sticky="nsew")
        self.lblScoreTIE.config(font=("Consolas", 14, "bold"), foreground="green")
        self.lblScoreTIE['text'] = str(self.scoreTIE)
        self.upperRightFrame.grid_columnconfigure([0, 1, 3, 4], weight=2)
        self.upperRightFrame.grid_columnconfigure([2], weight=1)

        # MAIN BOARD
        self.buttonBoard = []
        for i in range(0, 81):
            self.buttonBoard.append(Button(self.middleRightFrame, text=BLANK))

            # Separate buttons every 3 columns/rows
            ppadx = 1 if ((i % 9) % 3 == 1) else 9
            ppady = 1 if ((int(i / 9)) % 3 == 1) else 9
            self.buttonBoard[i].grid(row=int(i / 9), column=int(i % 9), padx=ppadx, pady=ppady, sticky="nsew")
            self.buttonBoard[i].config(height=1, font=("Consolas", 16, "bold"), state=DISABLED, )

            # Set commands
            self.buttonBoard[i].config(command=partial(self.commandBoardButton, i))
        self.middleRightFrame.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], weight=1)

        # MESSAGE AREA
        self.lblMsg = ttk.Label(self.bottomRightFrame, text="Waiting...", width=46, anchor="center")
        self.lblMsg.grid(row=0, column=0, padx=10, pady=10)
        self.lblMsg.config(font=("Consolas", 14), foreground="brown")
        self.bottomRightFrame.grid_columnconfigure([0], weight=1)

        # Progress bar
        self.progressBar = ttk.Progressbar(self.bottomRightFrame, orient=HORIZONTAL, length=400)
        self.progressBar.config(mode='determinate', maximum=10, value=0)
        self.progressBar.grid(row=1, column=0, padx=10, pady=10)

        # PARAMETERS
        # Play button
        self.buttonPlay = Button(self.upperLeftFrame, text="Play a New Game")
        self.buttonPlay.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.buttonPlay.config(height=1, font=("Consolas", 14, "bold"), command=self.commandPlayButton)
        self.upperLeftFrame.grid_columnconfigure([0], weight=1)

        # Reset button
        self.buttonReset = Button(self.upperLeftFrame, text="Reset")
        self.buttonReset.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.buttonReset.config(height=1, font=("Consolas", 14, "bold"), command=self.commandResetButton)

        # Depth configuration
        self.lblScale = ttk.Label(self.upperLeftFrame, text="Max Depth Analysis", width=30, anchor="center",
                                  font=("Consolas", 14, "bold"), foreground="dark gray")
        self.lblScale.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.depthAnalysis = DoubleVar()
        self.scaleDepth = Scale(self.upperLeftFrame, orient=HORIZONTAL, length=300, variable=self.depthAnalysis,
                                from_=1.0, to=9.0, showvalue=True)
        self.scaleDepth.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.scaleDepth.set(5.0)

        # Max number of iterations
        self.lblMaxIter = ttk.Label(self.upperLeftFrame, text="Max Iterations".ljust(16, ".") + "0".rjust(8, "."),
                                    width=24, font=("Consolas", 14, "bold"), foreground="dark gray")
        self.lblMaxIter.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        # Max depth reached
        self.lblMaxDepth = ttk.Label(self.upperLeftFrame, text="Max Depth".ljust(16, ".") + "0".rjust(8, "."), width=24,
                                     font=("Consolas", 14, "bold"), foreground="dark gray")
        self.lblMaxDepth.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        # Best Score
        self.lblBestScore = ttk.Label(self.upperLeftFrame, text="Best Score ".ljust(16, ".") + "0".rjust(8, "."),
                                      width=24, font=("Consolas", 14, "bold"), foreground="dark gray")
        self.lblBestScore.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        # Moves info
        self.lblMoves = ttk.Label(self.upperLeftFrame, text="Moves Info", width=30, anchor="center",
                                  font=("Consolas", 14, "bold"), foreground="dark gray", justify=CENTER)
        self.lblMoves.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")

        # MOVES INFO
        self.buttonMove = []
        for localIndex in range(0, 9):
            self.buttonMove.append(Button(self.bottomLeftFrame, text="NA"))
            self.buttonMove[localIndex].grid(row=int(localIndex / 3), column=int(localIndex % 3), padx=15, pady=15,
                                             sticky="nsew")
            self.buttonMove[localIndex].config(height=3, font=("Consolas", 10), foreground="black", state=DISABLED,
                                               relief=GROOVE)
        self.bottomLeftFrame.grid_columnconfigure([0, 1, 2], weight=1)

        self.showGameStats()

    # Play button command
    def commandPlayButton(self):
        # Ask if the player wants to start the game
        answer = messagebox.askyesnocancel("New Play", "Do you want to start the game?")
        if (answer == True):
            self.currentPlayer = self.humanPlayer
        elif (answer == False):
            self.currentPlayer = self.computerPlayer
        else:
            return

        # Init Game Variables
        self.initGame()
        self.showGameStats()
        self.showComputerProcess()

        # Make the first move if it is computer's turn (random)
        if (self.currentPlayer == self.computerPlayer):
            self.makeMove(random.randint(0, 80))
            # Enable board buttons
            self.changeBoardButtonsState(enable=True)

    # Play button command
    def commandResetButton(self):
        # Ask if the player wants to start the game
        answer = messagebox.askyesno("New Play", "Do you want to reset the game?")
        if (answer):
            # Init ALL Game Variables
            self.initGame()
            self.scoreCP = 0
            self.scoreHP = 0
            self.scoreTIE = 0

            # Refresh the scren
            self.showGameStats()
            self.showComputerProcess()

            # Disable all board buttons
            self.changeBoardButtonsState(enable=False)
            self.lblMsg['text'] = "Waiting..."

    # Board button command
    def commandBoardButton(self, index):

        # Update max depth analysis variable
        self.maxDepth = int(self.scaleDepth.get())

        # Check if the game already ended
        if self.gameStatus != UNKNOWN: return

        # Accept click only if if is Human Player's turn
        if self.currentPlayer == self.humanPlayer:

            # Set cell value for clicked cell
            self.mainBoard[index] = self.currentPlayer

            # Make the move
            self.makeMove(index)

            # Disable buttons for Human Player
            self.changeBoardButtonsState(enable=False)

            # End of game ?
            if self.gameStatus != UNKNOWN: return

            # Computer's turn
            self.getComputerMove(index)

            # End of game?
            if self.gameStatus != UNKNOWN: return

            # Enable buttons for Human Player
            self.changeBoardButtonsState(enable=True)

    # Initializes all the instance variables of the game
    def initGame(self):
        # Initialize board
        for i in range(0, 81):
            self.mainBoard[i] = BLANK
            self.buttonBoard[i].config(state=NORMAL)
            self.buttonBoard[i].config(relief=RAISED)

        # Initializa moves evaluation
        for i in range(0, 9):
            self.buttonMove[i]['text'] = "NA"

        # Initialize computer control variables
        self.maxDepth = int(self.scaleDepth.get())
        self.iterations = 0
        self.depthReached = 0
        self.bestScore = 0
        self.progress = 0.0

        # Initialize game stats
        self.currentMove = 1
        self.lastMove = -1
        self.gameWinner = UNKNOWN
        self.gameStatus = UNKNOWN
        self.winnerLine = []

    # Enable / Disable board buttons
    def changeBoardButtonsState(self, enable=False):

        # Get the Sector to be enabled
        nextSectY = int((self.lastMove / 9) % 3)
        nextSectX = int(self.lastMove % 3)

        # Disable all
        for i in range(0, 81):
            self.buttonBoard[i].config(state=DISABLED)
            self.buttonBoard[i].config(relief=FLAT)

        # Enable only blank cells of the right Sector
        if enable:
            for y in range(0, 3):
                for x in range(0, 3):

                    # Calculate index (i)
                    i = int(((nextSectY * 3) + y) * 9 + (nextSectX * 3) + x)

                    # Enable empty cells
                    if self.mainBoard[i] == BLANK:
                        self.buttonBoard[i].config(state=NORMAL)
                        self.buttonBoard[i].config(relief=RAISED)

    # Shows score and board
    def showGameStats(self):
        # Update board texts
        for i in range(0, 81):
            self.buttonBoard[i]['text'] = self.mainBoard[i]

        # Update board colors
        for i in range(0, 81):
            if ((i % 9 in [0, 1, 2, 6, 7, 8] and int(i / 9) in [0, 1, 2, 6, 7, 8]) or (
                    i % 9 in [3, 4, 5] and int(i / 9) in [3, 4, 5])):
                self.buttonBoard[i].config(background="ghost white")
            else:
                self.buttonBoard[i].config(background="light steel blue")
            if i == self.lastMove:
                self.buttonBoard[i].config(background="light goldenrod")

        # Winner line
        if (self.gameStatus == WIN or self.gameStatus == LOSE) and self.lastMove >= 0:
            self.buttonBoard[self.winnerLine[0]].config(background="sky blue")
            self.buttonBoard[self.winnerLine[1]].config(background="sky blue")
            self.buttonBoard[self.winnerLine[2]].config(background="sky blue")

        # Message
        if self.gameStatus == UNKNOWN and self.lastMove >= 0:
            if (self.currentPlayer == self.humanPlayer):
                self.lblMsg['text'] = "Human Player's turn, click on a cell please"
            else:
                self.lblMsg['text'] = "Computer Player's turn, please wait..."
        else:
            self.lblMsg['text'] = "Waiting..."

        # Show scores
        self.lblScoreHP['text'] = str(self.scoreHP)
        self.lblScoreTIE['text'] = str(self.scoreTIE)
        self.lblScoreCP['text'] = str(self.scoreCP)

    # make a move in the board, increment numPlays, changes the turn, and checks if there is a winner
    def makeMove(self, index):

        # Update the main board
        self.mainBoard[index] = self.currentPlayer

        # Update last move
        self.lastMove = index

        # Current Sector values
        currSectY = int(index / 27)
        currSectX = int((index % 9) / 3)

        # Check game status
        self.gameStatus = self.evaluateBoard(self.mainBoard, self.currentPlayer, currSectY, currSectX,
                                             saveWinnerLine=True)

        # If game ends, update scores and game winner
        if self.gameStatus != UNKNOWN:
            if self.gameStatus == WIN:

                # Save winner player in the instance variable
                self.gameWinner = self.currentPlayer

                # Check who won/lose
                if (self.currentPlayer == self.computerPlayer):
                    self.scoreCP += 1
                    msg = "Computer player WINS!"
                else:
                    self.scoreHP += 1
                    msg = "Human player WINS!"

            if self.gameStatus == TIE:
                msg = "It's a TIE!"
                self.scoreTIE += 1

            # Show the result
            self.showGameStats()
            self.lblMsg['text'] = msg
            messagebox.showinfo(title="End of game", message=msg)

            # Disable buttons
            self.changeStateBoardButtons(enable=False)
            return

            # Increase number of moves
        self.currentMove += 1

        # Change turn
        self.currentPlayer = self.humanPlayer if (self.currentPlayer == self.computerPlayer) else self.computerPlayer

        # Show info
        self.showGameStats()

        # Evaluates a move in another board, returns WIN, LOSE or TIE based on the player passed as an argument

    # Receives the board , current player and sector to be evaluated
    def evaluateBoard(self, board, player, sectY, sectX, saveWinnerLine=False):
        # Check all the winning lines
        for w in self.winningLines:
            # Calculate indexes
            index0 = int(((sectY * 3) + int(w[0] / 3)) * 9 + (sectX * 3) + (w[0] % 3))
            index1 = int(((sectY * 3) + int(w[1] / 3)) * 9 + (sectX * 3) + (w[1] % 3))
            index2 = int(((sectY * 3) + int(w[2] / 3)) * 9 + (sectX * 3) + (w[2] % 3))

            if board[index0] == board[index1] == board[index2] and board[index0] != BLANK:
                if saveWinnerLine:
                    self.winnerLine = [index0, index1, index2]
                if board[index0] == player:
                    return WIN
                else:
                    return LOSE

        # Check if there are more empty cells to play in that Sector
        for y in range(0, 3):
            for x in range(0, 3):
                index = int(((sectY * 3) + y) * 9 + (sectX * 3) + x)
                if (board[index]) == BLANK:
                    return UNKNOWN

        return TIE

        # Shows moves evaluation with colors

    def showComputerProcess(self, moves={}):
        # Clear all evaluation buttons
        for i in range(0, 9):
            if i not in moves:
                self.buttonMove[i]['text'] = "NA"
                self.buttonMove[i].config(background="white")

                # Show the scores:
        if (len(moves) > 0):
            for index in moves:
                score = moves[index]["score"]
                # Show the score in the button
                if score == WIN:
                    self.buttonMove[index]['text'] = "Win"
                    self.buttonMove[index].config(background="light green")
                elif score == LOSE:
                    self.buttonMove[index]['text'] = "Lose"
                    self.buttonMove[index].config(background="salmon")
                elif score == TIE:
                    self.buttonMove[index]['text'] = "Tie"
                    self.buttonMove[index].config(background="light goldenrod")
                elif score == UNKNOWN:
                    self.buttonMove[index]['text'] = "???"
                    self.buttonMove[index].config(background="dark gray")

                    # show the progress bar
        self.progressBar['value'] = self.progress
        self.progressBar.update()

        # Show iterations, depth info and best score
        self.lblMaxIter['text'] = "Max Iterations".ljust(16, ".") + str(self.iterations).rjust(8, ".")
        self.lblMaxDepth['text'] = "Max Depth".ljust(16, ".") + str(self.depthReached).rjust(8, ".")
        self.lblBestScore['text'] = "Best score".ljust(16, ".") + str(self.bestScore).rjust(8, ".")

    # Makes computer move based on score evaluation
    def getComputerMove(self, index):
        allMoves = {}  # List of all possible moves
        bestMoves = {}  # List of best moves
        randomMove = []
        tobeAnalyzed = 0  # Number of moves to be analyzed
        analyzing = 0  # Current move to be analyzed
        score = 0

        # No more moves then return
        if (self.currentMove > self.totalMoves): return

        # Sector where we need to play next move
        nextSectY = int((index / 9) % 3)
        nextSectX = int(index % 3)

        # Calculating number of available cells to be analyzed
        for y in range(0, 3):
            for x in range(0, 3):
                i = int(((nextSectY * 3) + y) * 9 + (nextSectX * 3) + x)
                if self.mainBoard[i] == BLANK: tobeAnalyzed += 1
        self.lblMsg['text'] = 'Calculating, please wait...'

        # Initialize computer control variables
        self.iterations = 0
        self.depthReached = 0
        self.progress = 0
        self.bestScore = LOSE

        # Initialize local count
        localCount = 0

        # Main loop to evaluate remaining moves
        for y in range(0, 3):
            for x in range(0, 3):

                # Calculate board index (i)
                localIndex = int(((nextSectY * 3) + y) * 9 + (nextSectX * 3) + x)

                if self.mainBoard[localIndex] == BLANK:

                    # Make the move in the main board
                    self.mainBoard[localIndex] = self.computerPlayer

                    # Evaluate it
                    score = self.minMax(self.mainBoard, False, localIndex, 1, self.currentMove)

                    # Update best score
                    if score > self.bestScore: self.bestScore = score

                    # Increase progress counter
                    analyzing += 1
                    self.progress = float((analyzing / tobeAnalyzed) * 10)

                    # Add board index and scores to all possible moves
                    allMoves[localCount] = {"index": localIndex, "score": score}

                    # Show process results so far
                    self.showComputerProcess(allMoves)

                    # Undo last move from the mainboard
                    self.mainBoard[localIndex] = BLANK

                    # Increase local Count number
                localCount += 1

                # Filter the best moves
        bestMoves = dict(filter(lambda elem: elem[1]["score"] == self.bestScore, allMoves.items()))

        # Select from best moves
        if (4 in bestMoves):
            bestMoves = dict(filter(lambda elem: elem[0] == 4, bestMoves.items()))  # Prefer Center
        elif (0 in bestMoves or 2 in bestMoves or 6 in bestMoves or 8 in bestMoves):
            bestMoves = dict(filter(lambda elem: elem[0] in [0, 2, 6, 8], bestMoves.items()))  # Then Corners

        # Select randomly among possible moves
        for key in bestMoves:
            randomMove.append(bestMoves[key]["index"])
        selectedMove = randomMove[random.randint(0, len(bestMoves) - 1)]

        # Reset progress bar
        self.progressBar['value'] = 0
        self.progressBar.update()

        # Make the suggested move
        self.makeMove(selectedMove)

    # Minimax Algorithm
    def minMax(self, board, isMaximizing, index, depth, moveNum):
        score = 0
        bestScore = LOSE
        worstScore = WIN
        localBoard = board.copy()

        # Increase number of iterations
        self.iterations += 1

        # Check max depth analysis reached
        self.depthReached = depth if (depth > self.depthReached) else self.depthReached

        # Get current Sector and next Sector
        currSectY = int(index / 27)
        currSectX = int((index % 9) / 3)
        nextSectY = int((index / 9) % 3)
        nextSectX = int(index % 3)

        # Evaluate current move (using current Sector)
        score = self.evaluateBoard(localBoard, self.computerPlayer, currSectY, currSectX)

        # Max depth reached? game ended?
        if (score != UNKNOWN or depth >= self.maxDepth): return score

        # Check blank cells whithin the new Sector
        for y in range(0, 3):
            for x in range(0, 3):

                # Convert y and x to an index
                localIndex = int(((nextSectY * 3) + y) * 9 + (nextSectX * 3) + x)

                # Check if index is blank
                if (localBoard[localIndex] == BLANK):

                    # Play as computer or human based on isMaximining flag
                    localBoard[localIndex] = self.computerPlayer if (isMaximizing) else self.humanPlayer

                    # Recursively evaluate the move
                    score = self.minMax(localBoard, not isMaximizing, localIndex, depth + 1, moveNum + 1)

                    # Check if we have some score
                    if isMaximizing:
                        bestScore = score if (score > bestScore) else bestScore
                    else:
                        worstScore = score if (score < worstScore) else worstScore

                    # Undo last move
                    localBoard[localIndex] = BLANK

        # Return the score
        return bestScore if isMaximizing else worstScore


# Main funciton
def main():
    root = Tk()
    game = TTTExt(root)
    root.mainloop()
    # root2 = Tk()
    # game = TTTExt (root2)
    # root2.mainloop ()


if __name__ == "__main__":
    main()