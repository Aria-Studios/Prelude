from tkinter import *
from tkinter import ttk
import os, sys, webbrowser

import config

# functions to fully close the program at any point
def close():
    window.quit()
    sys.exit()

# enables all GUI options
def enable():
    actions.entryconfigure('Display Game Developer Messages', state=NORMAL)
    actions.entryconfigure('Download Latest Core', state=NORMAL)
    actions.entryconfigure('Download Latest Patch', state=NORMAL)
    updateButton['state'] = NORMAL
    if (config.authMethod != ''):
        if (os.path.exists(config.privateBuildChannelName) == True):
            privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build Patch', state=NORMAL)
            privateBuildChannel.entryconfigure('Remove ' + config.privateBuildChannelName + ' Build', state=NORMAL)
        else:
            if (config.authMethod == 'none' or os.path.exists(config.tokenFile) == True):
                privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build Core', state=NORMAL)
            else:
                privateBuildChannel.entryconfigure('Authorization', state=NORMAL)

# disables all GUI options
def disable():
    actions.entryconfigure('Display Game Developer Messages', state=DISABLED)
    actions.entryconfigure('Download Latest Core', state=DISABLED)
    actions.entryconfigure('Download Latest Patch', state=DISABLED)
    updateButton['state'] = 'disabled'
    if (config.authMethod != ''):
        privateBuildChannel.entryconfigure('Authorization', state=DISABLED)
        privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build Core', state=DISABLED)
        privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build Patch', state=DISABLED)
        privateBuildChannel.entryconfigure('Remove ' + config.privateBuildChannelName + ' Build', state=DISABLED)

# sets up the GUI
window = Tk()
window.title(config.gameTitle + ' Updater')
if (config.iconPath != '' and os.path.exists(config.iconPath) == True):
    window.iconbitmap(config.iconPath)
window.option_add('*tearOff', False)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.geometry('300x300')

# sets up the menu
menubar = Menu(window)
actions = Menu(menubar)
menubar.add_cascade(label='Actions', menu=actions)
actions.add_command(label='Update Game', command=None, state='disabled')
actions.add_command(label='Display Game Developer Messages', command=None, state='disabled')
actions.add_separator()
if (config.changelogURL != ''):
    actions.add_command(label='View Changelog', command=lambda: webbrowser.open(config.changelogURL))
else:
    actions.add_command(label='View Changelog', state='disabled')
actions.add_command(label='Download Latest Core', command=lambda: webbrowser.open(config.urlPath + '/' + config.coreArchive))
actions.add_command(label='Download Latest Patch', command=lambda: webbrowser.open(config.urlPath + '/' + config.patchArchive))
actions.add_separator()
actions.add_command(label='Close', command=close)
if (config.authMethod != ''):
    privateBuildChannel = Menu(menubar)
    menubar.add_cascade(label=config.privateBuildChannelName + ' Build Channel', menu=privateBuildChannel)
    privateBuildChannel.add_command(label='Authorization', command=None, state='disabled')
    privateBuildChannel.add_separator()
    privateBuildChannel.add_command(label='Install Latest ' + config.privateBuildChannelName + ' Build Core', command=None, state='disabled')
    privateBuildChannel.add_command(label='Install Latest ' + config.privateBuildChannelName + ' Build Patch', command=None, state='disabled')
    privateBuildChannel.add_command(label='Remove ' + config.privateBuildChannelName + ' Build', command=None, state='disabled')
about = Menu(menubar)
menubar.add_cascade(label='About', menu=about)
if (config.gameURL != ''):
    about.add_command(label='About ' + config.gameTitle, command=lambda: webbrowser.open(config.gameURL))
else:
    about.add_command(label='About ' + config.gameTitle, state='disabled')
about.add_command(label='About Prelude', command=lambda: webbrowser.open('https://gitlab.com/ariastudios/prelude'))
window.config(menu=menubar)

# displays the version information
mainFrame = ttk.Frame(window).grid(column=0, row=0)
versionFrame = ttk.Frame(mainFrame, width=300, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
ttk.Label(versionFrame, text='My Version:').grid(column=0, row=0, columnspan=1, rowspan=1, pady=10)
localVersionLabel = ttk.Label(versionFrame, text=0)
localVersionLabel.grid(column=1, row=0, columnspan=1, rowspan=1, padx=50, pady=10)
ttk.Label(versionFrame, text='Current Version:').grid(column=0, row=1, columnspan=1, rowspan=1, sticky=N, pady=10)
remoteVersionLabel = ttk.Label(versionFrame, text=0)
remoteVersionLabel.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

# displays the progressbar, progress label, and action buttons
updateFrame = ttk.Frame(mainFrame, width=300, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
progressBar = ttk.Progressbar(updateFrame, orient='horizontal', length=200, mode='determinate')
progressBar.grid(column=0, row=3, columnspan=2, rowspan=1, sticky=N, pady=10)
progressLabel = ttk.Label(updateFrame, text='Select an option below.')
progressLabel.grid(column=0, row=4, columnspan=2, rowspan=1, sticky=N, pady=3)
updateButton = ttk.Button(updateFrame, text='Update Game', command=None, state='disabled')
updateButton.grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)
closeButton = ttk.Button(updateFrame, text='Close', command=close).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)

# displays Prelude credits
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=7, columnspan=2, rowspan=1)
creditFrame = ttk.Frame(mainFrame, width=300, height=25).grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S)
ttk.Label(creditFrame, text='Powered by Prelude v3').grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S, pady=10)
