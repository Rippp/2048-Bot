from PIL import ImageGrab, ImageOps
import pyautogui, time, math


# Coordinates for every tile in a game
class Coordinates:
    # First row of tiles
    coordinate11 = (169, 300)
    coordinate12 = (240, 300)
    coordinate13 = (354, 300)
    coordinate14 = (496, 300)
    # Second row of tiles
    coordinate21 = (169, 410)
    coordinate22 = (275, 410)
    coordinate23 = (389, 410)
    coordinate24 = (496, 410)
    # Third row of tiles
    coordinate31 = (169, 521)
    coordinate32 = (270, 515)
    coordinate33 = (389, 521)
    coordinate34 = (496, 521)
    # Fourth row of tiles
    coordinate41 = (169, 633)
    coordinate42 = (275, 633)
    coordinate43 = (389, 633)
    coordinate44 = (496, 633)

    # Array of tiles coordinates
    coordinateArray = [coordinate11, coordinate12,
                       coordinate13, coordinate14,
                       coordinate21, coordinate22,
                       coordinate23, coordinate24,
                       coordinate31, coordinate32,
                       coordinate33, coordinate34,
                       coordinate41, coordinate42,
                       coordinate43, coordinate44]


# Grayscale value for every number
class Values:
    empty = 195
    two = 229
    four = 225
    eight = 190
    sixteen = 172
    threeTwo = 157
    sixFour = 135
    oneTwoEight = 205
    twoFiveSix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    # Array of grayscale values
    valueArray = [empty, two, four, eight,
                  sixteen, threeTwo, sixFour,
                  oneTwoEight, twoFiveSix, fiveOneTwo,
                  oneZeroTwoFour, twoZeroFourEight]


# Current values at the grid
currentGrid = [0,   0,   0,  0,
               0,   0,   0,  0,
               0,   0,   0,  0,
               0,   0,   0,  0]

# Constant values representing directions
UP = 100
DOWN = 101
LEFT = 102
RIGHT = 103
DIR = 0

# Updating the currentGrid array values using ImageGrab
def updateGrid():
    screenImage = ImageGrab.grab()
    grayScreenImage = ImageOps.grayscale(screenImage)
    for index, cord in enumerate(Coordinates.coordinateArray):
        pixel = grayScreenImage.getpixel(cord)
        try:
            position = Values.valueArray.index(pixel)
        except:
            #print(index)
            position = 0

        if position == 0:
            currentGrid[index] = 0
        else:
            currentGrid[index] = 2 ** position

# Swapping the given row from right to left
def swipeRow(row):
    previous = -1  # previous non-zero element
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0:
            if previous == -1:
                previous = element
                temp[i] = element
                i += 1
            elif previous == element:
                temp[i - 1] = 2 * element
                previous = -1
            else:
                previous = element
                temp[i] = element
                i += 1
    return temp

# Swapping the given grid in given direction
def swipeGrid(grid, direction):
    temp = [0,0,0,0,
            0,0,0,0,
            0,0,0,0,
            0,0,0,0]

    if direction == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4*j])

            row = swipeRow(row)

            for j in range(4):
                temp[i+4*j] = row[j]

    elif direction == DOWN:
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i + 4*j])
            row = swipeRow(row)
            k=0
            for j in range(3, -1, -1):
                temp[i+4*j] = row[k]
                k += 1

    elif direction == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i*4 + j])
            row = swipeRow(row)
            for j in range(4):
                temp[i*4 + j] = row[j]

    elif direction == RIGHT:
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i*4 + j])
            row = swipeRow(row)
            k = 0
            for j in range(3, -1, -1):
                temp[4*i + j] = row[k]
                k += 1
    return temp

# Checking if the move is possible
def movePossible(grid, direction):
    if grid == swipeGrid(grid, direction):
        return False
    else:
        return True

# Performing move
def performMove(move):
    if move == UP:
        print("Going UP")
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    if move == DOWN:
        print("Going DOWN")
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    if move == LEFT:
        print("Going LEFT")
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    if move == RIGHT:
        print("Going RIGHT")
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')

# Printing out given grid
def printGrid(grid):
    for i in range(4):
        row = []
        for j in range(4):
            row.append(grid[i*4 + j])
        print(row)

# Printing gray scale values for every point in Coordinates class
def printGrayscale():
    image = ImageGrab.grab()
    image = ImageOps.grayscale(image)
    for i in range(4):
        row = []
        for j in range(4):
            row.append(image.getpixel(Coordinates.coordinateArray[i*4 + j]))
        print(row)

# Heuristic giving bonus points for every empty tile on the board
def emptyTilesHeuristic(grid):
    zeros = 0
    for i in range(16):
        if grid[i] == 0:
            zeros += 1

    return zeros

# Heuristic giving bonus points for maximum value on the board
def maxValueHeuristic(grid):
    maximumValue = -1
    for i in range(16):
        maximumValue = max(maximumValue, grid[i])

    return maximumValue

# Heuristic giving bonus points for minimizing differences between adjacent tiles
def smoothnessHeuristic(grid):
    smoothness = 0
    for i in range(4):
        current = 0
        while current < 4 and grid[4*i + current] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1
            if next >= 4:
                break

            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    for i in range(4):
        current = 0
        while current < 4 and grid[current*4 + i] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[4*next + i]:
                next += 1
            if next >= 4:
                break

            currentValue = grid[current*4 + i]
            nextValue = grid[next*4 + i]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    return smoothness*10

# Heurisitc giving bonus poitns for monotonic rows of tiles
def monotonicityHeurictic(grid):
    monotonicityScores = [0, 0, 0, 0]

    # left/right direction
    for i in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1

            if next >= 4:
                next -= 1
            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]

            if currentValue > nextValue:
                monotonicityScores[0] += nextValue - currentValue
            elif nextValue > currentValue:
                monotonicityScores[1] += currentValue - nextValue

            current = next
            next += 1

    #up/down direction
        for i in range(4):
            current = 0
            next = current + 4
            while next < 4:
                while next < 4 and grid[i + 4*next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                currentValue = grid[i + 4*current]
                nextValue = grid[i + 4*next]

                if currentValue > nextValue:
                    monotonicityScores[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    monotonicityScores[3] += currentValue - nextValue
            current = next
            next += 1

    return 20* max(monotonicityScores[0], monotonicityScores[1]) + max(monotonicityScores[2], monotonicityScores[3])

# Heuristic giving bonus points for placing tile with maximum value at the corner of the board
def positionOfMaxValueHeuristic(grid):
    maxValue = maxValueHeuristic(grid)
    if maxValue == grid[0] or maxValue == grid[3] or maxValue == grid[12] or maxValue == grid[15]:
        return 5000
    else:
        return -5000

# Heuristic using weighted grid to determine how many bonus points we are supposed to give
def weightedTilesHeuristic(grid):
    scoreGrid = [4**15, 4**14, 4**13, 4**12,
                 4**8,  4**9,  4**10, 4**11,
                 4**7,  4**6,  4**5,  4**4,
                 4**0,  4**1,  4**2,  4**3]

    score = 0
    for i in range(16):
        score += grid[i] * scoreGrid[i]

    return score


# Function returning score of the given graph   
# Feel free to modify it and play with the constants :)
def getScore(grid):
    emptyTilesScore = emptyTilesHeuristic(grid) * 100
    maxValueScore = maxValueHeuristic(grid) * 4
    smoothnessScore = smoothnessHeuristic(grid) * 10
    monotonicityScore = monotonicityHeurictic(grid) * 40
    positionOfMaxValueScore = positionOfMaxValueHeuristic(grid) * 5
    weightedTilesScore = weightedTilesHeuristic(grid)

    # Exemplary score, try to modify it along with constants above
    # Little change can make huge difference
    return weightedTilesScore + smoothnessScore + emptyTilesScore