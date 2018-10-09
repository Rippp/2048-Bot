# 2048-Bot

Just a simple implementation of a game bot designed to play 2048 game. It uses MiniMax algorithm with Alpha-Beta pruning. Feel free to test it yourself and modify it to see some interesting changes in performance and behaviour.

## Prerequisites

You wil need to have Python 3.6 installed with the following libraries: Pillow and pyautogui

Bot imports data from the game interface by using image grab from Pillow library. To make it work you have to overwrite coordinates for every tile on the board. You can use mouse.py to display position of your cursor. Coordinates of every tile are in grid.py file. This thing has to be done beacuse cooridinates may vary on different screen resolutions.
