from AI import *

def main():
    # Giving time necessary to change focus to the browser
    time.sleep(3)

    # Playing the game.
    # Have fun experimenting on your own and try changing heuristics in grid.py to see the difference in performance :)
    while 1:
        updateGrid()
        createMiniMaxTree(2)
        performMove(getMoves())

if __name__ == '__main__':
    main()
