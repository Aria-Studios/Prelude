from tkinter import *
from tkinter import ttk

import config, gui

def authWindow():
    authWindow = Toplevel(gui.window)
    authWindow.title(config.gameTitle + ' ' + config.privateBuildChannelName + ' Build Channel Authorization')
    authWindow.geometry('300x300')
