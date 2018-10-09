from grid import *

# Array containing score for every node in MiniMaxTree
nodeScores = [0 for x in range(50000)]
# Array containing child node numbers for every node in MinMaxTree
childList = [[0 for x in range(0)] for y in range(50000)]
# Global counter for actual node number
nodeNumber = 1
# Array of constants for directions
directions = [100, 101, 102, 103]

# Clears above arrays and making MiniMaXTree of given depth
def createMiniMaxTree(depth):
    global nodeScores
    global childList
    global alphaBetaScores
    global nodeNumber
    nodeScores = [0 for x in range(50000)]
    childList = [[0 for x in range(0)] for y in range(50000)]
    nodeNumber = 1

    alphaBetaPruning(1, currentGrid, 0, depth, -math.inf, math.inf)

# Creating MiniMaxTree with alpha - beta pruning
def alphaBetaPruning(node, grid, parent, depth, alpha, beta):
    global nodeScores
    global childList
    global nodeNumber

    # Terminal state
    if depth == 0:
        nodeScores[node] = getScore(grid)
        return nodeScores[node]

    # The turn of the player. I am making a new node for every possible move
    if depth%2 == 0:

        for i in range(4):
            nodeNumber += 1
            childList[node].append(nodeNumber)
            if(movePossible(grid, directions[i])) == True:
                alpha = max(alpha, alphaBetaPruning(nodeNumber, swipeGrid(grid, directions[i]), node, depth-1, alpha, beta))
            if alpha >= beta:
                break
        nodeScores[node] = alpha
        return alpha

    # The turn of the computer. I am looking through every possible outcome and picking up the worst ones
    else:
        zeros = []
        for i in range(16):
            if grid[i] == 0:
                zeros.append(i)

        gridTable = [[0 for x in range(16)] for y in range(0) ]
        gridTableScores = []

        for i in zeros:
            grid[i] = 2
            gridTable.append(grid)
            grid[i] = 0

        for i in zeros:
            grid[i] = 4
            gridTable.append(grid)
            grid[i] = 0

        for i in gridTable:
            gridTableScores.append(getScore(i))

        for i in range(4):
            minimumScore = min(gridTableScores)
            indeks = gridTableScores.index(minimumScore)

            nodeNumber += 1
            childList[node].append(nodeNumber)
            beta = min(beta, alphaBetaPruning(nodeNumber, gridTable[indeks], node, depth-1, alpha, beta))

            if beta <= alpha:
                break

            gridTableScores[indeks] = math.inf

        nodeScores[node] = beta
        return beta

# Returning the best move to perform
def getMoves():
    searchedValue = nodeScores[1]

    for index, i in enumerate(childList[1]):
        if nodeScores[i] == searchedValue:
            return directions[index]