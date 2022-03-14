# # # # # # # # # # # # # #
#         Prelude         #
# # # # # # # # # # # # # #
# START FILE EDITING HERE #
# # # # # # # # # # # # # #

# Title of your game
gameTitle = 'Game Title'

# A URL link to your game's information
gameURL = 'https://reliccastle.com'

# The URL path to where the remote files are stored, NO TRAILING SLASHES
urlPath = 'https://domain.com/downloads'

# The version file name, NO STARTING OR TRAILING SLASHES
versionFile = 'version'

# The patch file name, MUST BE ZIP FORMAT
patchArchive = 'patch.zip'

# The core file name, MUST BE ZIP format
coreArchive = 'core.zip'

# # # # # # # # # # # # # #
#  END FILE EDITING HERE  #
# # # # # # # # # # # # # #

# import relevant libraries
# tkinter for GUI, webbrowser to launch menu links
# threading for progressbar, urllib for checking the current version
# requests to download the patch, zipfile to unzip the patch
# os to delete patch zip when done
from tkinter import *
from tkinter import ttk
import webbrowser
import threading
import urllib.request
import requests
from zipfile import ZipFile
import os

# reads the local version file to get the version number, converts it to a float, returns result to function call
def getMyVersion():

    file = open(versionFile, 'r')
    myVersion = float(file.read())
    file.close()

    return myVersion

# retrieves the remote version file to get the version number, converts it to a float, returns result to function call
def getCurrentVersion():

    currentVersion = float(urllib.request.urlopen(urlPath + '/' + versionFile).read())

    return currentVersion

# checks to see how versions compare. first case should download both the latest core and then the patch.
# second case should just download the latest core. third case should just download the latest patch.
# fourth case shouldn't happen at all.
def updateGame():

    if (int(myVersion) < int(currentVersion) and int(currentVersion) != currentVersion):
        progressLabel['text'] = 'Downloading latest core.'

        file = open(coreArchive, 'wb')
        zip = requests.get(urlPath + '/' + coreArchive)
        file.write(zip.content)
        file.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Unzipping core file.'

        file = ZipFile(coreArchive, 'r')
        file.extractall()
        file.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Removing core file.'

        os.remove(coreArchive)

        progressBar['value'] += 10
        progressLabel['text'] = 'Downloading latest patch.'

        file = open(patchArchive, 'wb')
        zip = requests.get(urlPath + '/' + patchArchive)
        file.write(zip.content)
        file.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Unzipping patch file.'

        file = ZipFile(patchArchive, 'r')
        file.extractall()
        file.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Removing patch file.'

        os.remove(patchArchive)

        progressBar['value'] += 10
        progressLabel['text'] = gameTitle + ' is now up to date!'
    elif (int(myVersion) < int(currentVersion) and int(currentVersion) == currentVersion):
        progressLabel['text'] = 'Downloading latest core.'

        file = open(coreArchive, 'wb')
        zip = requests.get(urlPath + '/' + coreArchive)
        file.write(zip.content)
        file.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Unzipping core file.'

        file = ZipFile(coreArchive, 'r')
        file.extractall()
        file.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Removing core file.'

        os.remove(coreArchive)

        progressBar['value'] += 20
        progressLabel['text'] = gameTitle + ' is now up to date!'
    elif (myVersion < currentVersion):
        progressLabel['text'] = 'Downloading latest patch.'

        file = open(patchArchive, 'wb')
        zip = requests.get(urlPath + '/' + patchArchive)
        file.write(zip.content)
        file.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Unzipping patch file.'

        file = ZipFile(patchArchive, 'r')
        file.extractall()
        file.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Removing patch file.'

        os.remove(patchArchive)

        progressBar['value'] += 20
        progressLabel['text'] = gameTitle + ' is now up to date!'
    else:
        progressBar['value'] = 100
        progressLabel['text'] = 'Error.'

    newVersion = getMyVersion()

    myVersionLabel['text'] = format(newVersion, '.2f')
    actions.entryconfigure('Update Game', state=DISABLED)
    updateButton['state'] = 'disabled'

# calls relevant functions for initial information
myVersion = getMyVersion()
currentVersion = getCurrentVersion()

# sets up the GUI
window = Tk()
window.title(gameTitle + ' Updater')
window.option_add('*tearOff', False)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# sets up the menu
menubar = Menu(window)
actions = Menu(menubar)
menubar.add_cascade(label='Actions', menu=actions)
actions.add_command(label='Update Game', command=lambda: threading.Thread(target=updateGame).start())
actions.add_separator()
actions.add_command(label='Download Latest Core', command=lambda: webbrowser.open(urlPath + '/' + coreArchive))
actions.add_command(label='Download Latest Patch', command=lambda: webbrowser.open(urlPath + '/' + patchArchive))
actions.add_separator()
actions.add_command(label='Close', command=window.destroy)
about = Menu(menubar)
menubar.add_cascade(label='About', menu=about)
about.add_command(label='About ' + gameTitle, command=lambda: webbrowser.open(gameURL))
about.add_command(label='About Prelude', command=lambda: webbrowser.open('https://gitlab.com/ariastudios/prelude'))

# displays the version information
mainFrame = ttk.Frame(window).grid(column=0, row=0)
versionFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
ttk.Label(versionFrame, text='My Version:').grid(column=0, row=0, columnspan=1, rowspan=1, sticky=N, pady=10)
myVersionLabel = ttk.Label(versionFrame, text=format(myVersion, '.2f'))
myVersionLabel.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Label(versionFrame, text='Current Version:').grid(column=0, row=1, columnspan=1, rowspan=1, sticky=N, pady=10)
ttk.Label(versionFrame, text=format(currentVersion, '.2f')).grid(column=1, row=1, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

# displays the progressbar, progress label, and action buttons
updateFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
progressBar = ttk.Progressbar(updateFrame, orient='horizontal', length=200, mode='determinate')
progressBar.grid(column=0, row=3, columnspan=2, rowspan=1, sticky=N, pady=10)
progressLabel = ttk.Label(updateFrame, text='Select an option below.')
progressLabel.grid(column=0, row=4, columnspan=2, rowspan=1, sticky=N, pady=3)

if (myVersion < currentVersion):
    updateButton = ttk.Button(updateFrame, text='Update Game', command=lambda: threading.Thread(target=updateGame).start())
    updateButton.grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)
else:
    updateButton = ttk.Button(updateFrame, text='Update Game', state='disabled').grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)

closeButton = ttk.Button(updateFrame, text='Close', command=window.destroy).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)

# displays Prelude credits
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=7, columnspan=2, rowspan=1)
creditFrame = ttk.Frame(mainFrame, width=250, height=25).grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S)
ttk.Label(creditFrame, text='Powered by Prelude').grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S, pady=10)

# creates & displays the full GUI
window.config(menu=menubar)
window.mainloop()
