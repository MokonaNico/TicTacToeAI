import os
from copy import deepcopy
from random import shuffle, choice
import math
import colorama
from colorama import Fore
import matplotlib.pyplot as plt

colorama.init()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:
    def __init__(self, name, num, symbol, color):
        self.name = name
        self.state = None
        self.symbol = symbol  # O or X
        self.num = num
        self.color = color

    def __str__(self):
        if self.state:
            return ">" + self.color + self.name + Fore.RESET
        return " " + self.color + self.name + Fore.RESET

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.num == other.num

    def changePlayerState(self, other):
        if self.state is None and other.state is None:
            self.state = True
            other.state = False
        elif self.state is True and other.state is False:
            self.state = False
            other.state = True
        else:
            self.state = True
            other.state = False


class Human(Player):
    def getNextMove(self, grid):
        x = 0
        y = 0
        input_player = True
        while input_player:
            coord = input("Choose a square: ")
            coord = coord.split()
            if len(coord) == 2:
                try:
                    x = int(coord[0])
                    y = int(coord[1])
                    if grid.inBound((x, y)) and not grid.grid[y][x].isActivated():
                        break
                    else:
                        print("Invalid coordinate")
                except ValueError:
                    print("Invalid coordinate")
                    continue
            else:
                print("Invalid coordinate")
                continue
        return x, y


class AI(Player):
    def __init__(self, name, num, symbol, color, maxDepth):
        super().__init__(name, num, symbol, color)
        self.maxDepth = maxDepth

    def miniMax(self, maximizingPlayer, grid, alpha, beta, depth):
        if grid.getWinner() is not None:
            if maximizingPlayer:
                return -1 * (len(grid.getInactiveSquare()) + 1)
            else:
                return 1 * (len(grid.getInactiveSquare()) + 1)
        elif (len(grid.getInactiveSquare()) == 0) or (depth == self.maxDepth):
            return 0

        if maximizingPlayer:
            maxEval = -math.inf
            for square in grid.getInactiveSquare():
                grid.activateSquare(square.coord, self)
                evaluation = self.miniMax(False, grid, alpha, beta, depth + 1)
                grid.deactivateSquare(square.coord)
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = math.inf
            for square in grid.getInactiveSquare():
                grid.activateSquare(square.coord, grid.getOpponentFor(self))
                evaluation = self.miniMax(True, grid, alpha, beta, depth + 1)
                grid.deactivateSquare(square.coord)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval

    def getNextMove(self, grid):
        if len(grid.getInactiveSquare()) == 9:
            return 0, 0
        maximum = -math.inf
        coord = None
        copyGrid = deepcopy(grid)
        for square in grid.getInactiveSquare():
            copyGrid.activateSquare(square.coord, self)
            evaluation = self.miniMax(False, copyGrid, -math.inf, +math.inf, 0)
            copyGrid.deactivateSquare(square.coord)
            if evaluation > maximum:
                maximum = evaluation
                coord = square.coord
        return coord


class AIDumb(Player):
    def getNextMove(self, grid):
        return choice(grid.getInactiveSquare()).coord


class Square:

    def __init__(self, coord):
        self.coord = coord
        self.state = False
        self.repr = " "
        self.player = None

    def __str__(self):
        return self.repr

    def activate(self, player):
        self.repr = player.color + player.symbol + Fore.RESET
        self.state = True
        self.player = player

    def deactivate(self):
        self.repr = " "
        self.state = False
        self.player = None

    def isActivated(self):
        return self.state is True

    def getX(self):
        return self.coord[0]

    def getY(self):
        return self.coord[1]


class TicTacToe:

    def __init__(self, playerList):
        self.dim = 3
        self.grid = TicTacToe.createGrid(self.dim)
        self.playerList = playerList

    def __str__(self):
        strGrid = "-------------\n"
        for i in range(self.dim):
            strGrid += "| "
            for j in range(self.dim):
                strGrid += self.grid[i][j].__str__() + " | "
            strGrid += "\n-------------\n"
        return strGrid

    def createGrid(cls, dim):
        grid = []
        for i in range(dim):
            subGrid = []
            for j in range(dim):
                subGrid.append(Square((j, i)))
            grid.append(subGrid)
        return grid

    createGrid = classmethod(createGrid)

    def inBound(self, coord):
        x, y = coord
        return 0 <= x < self.dim and 0 <= y < self.dim

    def activateSquare(self, coord, player):
        x, y = coord
        if self.inBound(coord) and not (self.grid[y][x].isActivated()):
            self.grid[y][x].activate(player)

    def deactivateSquare(self, coord):
        x, y = coord
        if self.inBound(coord) and (self.grid[y][x].isActivated()):
            self.grid[y][x].deactivate()

    def copyTicTacToe(self):
        newTTT = TicTacToe(self.playerList)
        newTTT.grid = deepcopy(self.grid)
        return newTTT

    def getWinner(self):

        for i in range(self.dim):
            if (self.grid[i][0].player == self.grid[i][1].player == self.grid[i][2].player) and \
                    (self.grid[i][0].state and self.grid[i][1].state and self.grid[i][2].state):
                return self.grid[i][0].player
        for j in range(self.dim):
            if self.grid[0][j].player == self.grid[1][j].player == self.grid[2][j].player and \
                    (self.grid[0][j].state and self.grid[1][j].state and self.grid[2][j].state):
                return self.grid[0][j].player
        if (self.grid[0][0].player == self.grid[1][1].player == self.grid[2][2].player) and \
                (self.grid[0][0].state and self.grid[1][1].state and self.grid[2][2].state):
            return self.grid[1][1].player
        if self.grid[0][2].player == self.grid[1][1].player == self.grid[2][0].player and \
                (self.grid[0][2].state and self.grid[1][1].state and self.grid[2][0].state):
            return self.grid[1][1].player
        return None

    def getOpponentFor(self, player):
        if player.__eq__(self.playerList[0]):
            return self.playerList[1]
        return self.playerList[0]

    def getInactiveSquare(self):
        validSquare = []
        for y in range(3):
            for x in range(3):
                sq = self.grid[x][y]
                if not sq.isActivated():
                    validSquare.append(sq)
        return validSquare


def pickColor():
    list1 = [Fore.LIGHTBLACK_EX, Fore.BLUE, Fore.CYAN,
             Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.GREEN, Fore.LIGHTGREEN_EX]

    list2 = [Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX,
             Fore.LIGHTWHITE_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

    symbol = ["X", "O"]
    for i in range(10):
        shuffle(list1)
        shuffle(list2)
        shuffle(symbol)
    return list1[0], symbol[0], list2[0], symbol[1]


def game(player1, player2, printOn):
    playerList = [player1, player2]
    grid = TicTacToe(playerList)
    gameOn = True
    winner = None
    while gameOn:
        for player in playerList:
            playerList[0].changePlayerState(playerList[1])
            if printOn:
                clear()
                print(grid)
                print("{}\n{}".format(playerList[0], playerList[1]))
            if len(grid.getInactiveSquare()) == 0:
                gameOn = False
                break
            nextCoord = player.getNextMove(grid)
            grid.activateSquare(nextCoord, player)
            winner = grid.getWinner()
            if winner is not None:
                gameOn = False
                break
    if printOn:
        clear()
        print(grid)
    if winner is None:
        if printOn:
            print("Nobody wins...")
        return 0
    else:
        if printOn:
            print("{} wins !".format(winner))
        return winner.num


def setPlayers():
    inputPlayer = True
    mode = None

    while inputPlayer:
        print("Select a mode:\n\t\t1.Player vs Player\n\t\t2.Player vs AI\n\t\t3.AI vs AI\n")
        mode = input()
        try:
            mode = int(mode)
            if 1 <= mode <= 3:
                inputPlayer = False
        except ValueError:
            continue
    color1, symbol1, color2, symbol2 = pickColor()

    if mode == 2:
        name1 = input("Player name: ")
        p1 = Human(name1, 1, symbol1, color1)
        p2 = AI("BOT", -1, symbol2, color2, 9)
    elif mode == 1:
        name1 = input("Player 1 name: ")
        p1 = Human(name1, 1, symbol1, color1)
        name2 = input("Player 2 name: ")
        p2 = Human(name2, -1, symbol2, color2)
    elif mode == 3:
        p1 = AIDumb("BOT1", 1, symbol1, color1)
        p2 = AI("BOT2", -1, symbol2, color2, 9)
    return p1, p2


def stat(ia1, ia2, nbrOfGame):
    statDic = {"draw": 0, "ia1": 0, "ia2": 0}
    for n in range(nbrOfGame):
        g = game(ia1, ia2, False)
        if g == 0:
            statDic["draw"] += 1
        elif g == 1:
            statDic["ia1"] += 1
        elif g == -1:
            statDic["ia2"] += 1
    return statDic


def stat2(nbrOfGame):
    result = []
    color1, symbol1, color2, symbol2 = pickColor()
    for i in range(8):
        ia1 = AIDumb("BOT1", 1, symbol1, color1)
        ia2 = AI("BOT2", -1, symbol2, color2, i)
        result.append(stat(ia1, ia2, nbrOfGame)["ia1"])
        print("O", end="")
    plt.xlim([1, 8])
    plt.plot(result)
    plt.show()


if __name__ == "__main__":
    p1, p2 = setPlayers()
    game(p1, p2, True)
