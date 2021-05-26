import pyautogui
from pyautogui import *
from time import sleep

def oldevent():
    pyautogui.moveTo(485, 69)
    pyautogui.click()
    sleep(0.1)
    pyautogui.moveTo(864, 750) #king
    pyautogui.click()
    pyautogui.moveTo(821, 422) #drop king
    pyautogui.click()
    pyautogui.moveTo(864, 750) #ability
    pyautogui.click()
    pyautogui.moveTo(950, 750) #queen
    pyautogui.click()
    pyautogui.moveTo(822, 404) #drop queen
    pyautogui.click()
    pyautogui.moveTo(950, 750) #ability
    pyautogui.click()
    pyautogui.moveTo(1080, 750) #Rc
    pyautogui.click()
    pyautogui.moveTo(821, 422) #drop rc
    pyautogui.click()
    pyautogui.moveTo(1080, 750) #ability
    pyautogui.click()
    sleep(2)
    pyautogui.moveTo(547, 657)
    pyautogui.click()
    pyautogui.moveTo(1064, 603)
    pyautogui.click()
    sleep(0.1)
    pyautogui.moveTo(849, 676)
    pyautogui.click()
    pyautogui.moveTo(1070, 250)
    pyautogui.click()

def newevent():
    moveTo(155, 1003)
    click()
    moveTo()

if __name__ == "__main__":
    newevent()
