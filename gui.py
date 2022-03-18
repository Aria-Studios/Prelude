from tkinter import *
from tkinter import ttk
import sys, webbrowser

import config

# functions to fully close the program at any point
def close():
    window.quit()
    sys.exit()

# updates the progress bar based on the passed variable
def updatePBar(updateType):
    if (updateType == 'both'):
        progressBar['value'] += 17
    elif (updateType == 'core'):
        progressBar['value'] += 34
    elif (updateType == 'patch'):
        progressBar['value'] += 34

# sets up the GUI
window = Tk()
window.title(config.gameTitle + ' Updater')
window.option_add('*tearOff', False)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# sets up the menu
menubar = Menu(window)
actions = Menu(menubar)
menubar.add_cascade(label='Actions', menu=actions)
actions.add_command(label='Update Game', command=None, state='disabled')
actions.add_command(label='Display Game Developer Messages', command=None, state='disabled')
actions.add_separator()
actions.add_command(label='Download Latest Core', command=lambda: webbrowser.open(config.urlPath + '/' + config.coreArchive))
actions.add_command(label='Download Latest Patch', command=lambda: webbrowser.open(config.urlPath + '/' + config.patchArchive))
actions.add_separator()
actions.add_command(label='Close', command=close)
about = Menu(menubar)
window.config(menu=menubar)
menubar.add_cascade(label='About', menu=about)
if (config.gameURL != ''):
    about.add_command(label='About ' + config.gameTitle, command=lambda: webbrowser.open(config.gameURL))
else:
    about.add_command(label='About ' + config.gameTitle, command=lambda: webbrowser.open(config.gameURL), state='disabled')
about.add_command(label='About Prelude', command=lambda: webbrowser.open('https://gitlab.com/ariastudios/prelude'))

# displays the version information
mainFrame = ttk.Frame(window).grid(column=0, row=0)
versionFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
ttk.Label(versionFrame, text='My Version:').grid(column=0, row=0, columnspan=1, rowspan=1, sticky=N, pady=10)
localVersionLabel = ttk.Label(versionFrame, text=0)
localVersionLabel.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Label(versionFrame, text='Current Version:').grid(column=0, row=1, columnspan=1, rowspan=1, sticky=N, pady=10)
remoteVersionLabel = ttk.Label(versionFrame, text=0)
remoteVersionLabel.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

# displays the progressbar, progress label, and action buttons
updateFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
progressBar = ttk.Progressbar(updateFrame, orient='horizontal', length=200, mode='determinate')
progressBar.grid(column=0, row=3, columnspan=2, rowspan=1, sticky=N, pady=10)
progressLabel = ttk.Label(updateFrame, text='Select an option below.')
progressLabel.grid(column=0, row=4, columnspan=2, rowspan=1, sticky=N, pady=3)
updateButton = ttk.Button(updateFrame, text='Update Game', command=None, state='disabled')
updateButton.grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)
closeButton = ttk.Button(updateFrame, text='Close', command=close).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)

# displays Prelude credits
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=7, columnspan=2, rowspan=1)
creditFrame = ttk.Frame(mainFrame, width=250, height=25).grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S)
ttk.Label(creditFrame, text='Powered by Prelude v2').grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S, pady=10)
