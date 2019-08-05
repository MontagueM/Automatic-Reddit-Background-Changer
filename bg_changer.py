import ctypes
import os


def change_bg():
    cwd = os.getcwd()  # Getting current working directory
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd + "/background.png", 3)  # Setting background for all four monitors
    print("Changed image\n")
