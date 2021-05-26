import time 
import pyautogui
import pywinauto.win32functions
import win32gui
from win32gui import FindWindow as FW
from win32gui import EnumWindows as EW
from win32gui import MoveWindow as MW
from win32gui import GetWindowRect as GWR


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        global z
        z.append((hwnd, win32gui.GetWindowText(hwnd)))


def players(lstt) -> list:
    lstt = [i for i in lstt if "LD" in i and i != "LDMultiPlayer"]
    arr = ['Nox(64)', 'Nox-1(64)', 'Nox-2(64)', 'Nox-3(64)', 'Nox-4(64)', 'Nox-5(64)', 'Nox-6(64)',
           'Nox-7(64)', 'Nox-8(64)', 'Nox-9(64)', 'Nox-10(64)', 'Nox-11(64)', 'Nox-12(64)']
    lstt = [x for _, x in sorted(
        zip(arr, lstt), key=lambda pair: pair[0], reverse=True)]
    return lstt


def resize4lst(lstt) -> int:
    tx, ty, bx, by = 0, 0, 2560, 1394
    end1, end2 = 626+48, 351+27
    array = [(tx, ty, end1, end2), (end1, ty, end1, end2), (end1*2, ty, end1, end2),
             (tx, end2, end1, end2), (end1, end2,
                                      end1, end2), (end1*2, end2, end1, end2),
             (tx, end2*2, end1, end2), (end1, end2*2,
                                        end1, end2), (end1*2, end2*2, end1, end2),
             (tx, end2*3, end1, end2), (end1, end2*3, end1, end2), (end1*2, end2*3, end1, end2)]
    for win in range(len(lstt)):
        hwnd = FW(None, lstt[win])
        MW(hwnd, array[win][0], array[win][1],
           array[win][2], array[win][3], True)
    return 0


while True:
    z = []
    EW(winEnumHandler, None)
    z = [i for i in z if i[1] and 'BlueStacks' in i[1] and "Multi" not in i[1] and "Keymap" not in i[1]]
    '''z2 = sorted(players(z))
    resize4lst(z2)'''
    print(z)
    inp = input()
    if inp.lower() not in ['y', 'yes', 'ye']:
        break
    for i in z:
        try:
            pyautogui.press("alt")
            win32gui.SetForegroundWindow(i[0])
        except Exception as e:
            print(repr(e))
            continue


