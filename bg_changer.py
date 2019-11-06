import ctypes
import os


def change_bg():
    """
    Uses in-built OS commands to change the background. Only works for Windows as of now.
    """
    cwd = os.getcwd()  # Getting current working directory
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd + "/background.png", 3)  # Setting background for all four monitors
    print("Changed image\n")
