import pyautogui

# A simple program to check the coordinates of a mouse cursor
# The coordinates of the tiles should be written in the Coordinates class in grid.py
# It is necessary to do that before running a bot, because coordinates vary on different screen resolutions

while True:
    print(pyautogui.displayMousePosition())
