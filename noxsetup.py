import os, sys
from pyautogui import *
from time import sleep
args = sys.argv
print(sys.argv)
url = ''

def moveandclick(x1, y1, mode, clk=1, word=""):
    moveTo(1200, 600)
    xf = 814
    yf = 460
    x_list = [x1, x1+xf, x1+xf+xf]
    y_list = [y1, y1+yf, y1+yf+yf]
    arr = []
    if mode == 1:
        for x in x_list:
            for y in y_list:
                arr.append((x, y))
    elif mode == 2:
        for y in y_list:
            for x in x_list:
                arr.append((x, y))
    for coor in arr:
        a, b = coor
        moveTo(a, b)
        if word:
            click()
            write(word, interval=0.02)
            press('enter')
        else:
            click()
            if clk == 2:
                click()

while (current := input("Write something: ")) != "quit":
    if current == "1": #open apk folder and install 
        moveandclick(792, 247, 1)
        sleep(3)
        moveandclick(255, 413, 2, 2)

    elif current == "2": #open game
        moveandclick(554, 165, 2)

    elif current == "3": #click out of popup
        moveandclick(504, 115, 2, 2)

    elif current == "4": #go home
        moveandclick(790, 399, 2)

    elif current == "5": #menu tab button to clear app then back home to open game
        moveandclick(791, 441, 2)
        moveandclick(566, 140, 2)
        moveandclick(790, 399, 2)

    elif current == "6": #open browser
        moveandclick(99, 159, 2)

    elif current == "7": #write url 
        moveandclick(131, 71, 2, 1, '')

    elif current == "8": #open url
        moveandclick(393, 311, 2)

    elif current == "9": #open chat
        moveandclick(750, 45, 2)

    elif current == "10": #get to acc info page
        moveandclick(43, 419, 2)
        sleep(1)
        moveandclick(379, 384, 2)
