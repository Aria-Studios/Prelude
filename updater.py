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
urlPath = 'https://media.ariastudio.dev/prelude'

# The message file name, NO STARTING OR TRAILING SLASHES
messageFile = 'message'

# The version file name, NO STARTING OR TRAILING SLASHES
versionFile = 'version'

# The core file name, MUST BE ZIP format
coreArchive = 'core.zip'

# The patch file name, MUST BE ZIP FORMAT
patchArchive = 'patch.zip'

# # # # # # # # # # # # # #
#  END FILE EDITING HERE  #
# # # # # # # # # # # # # #

# import relevant modules
# tkinter for GUI, webbrowser to launch menu links
# threading for progressbar, urllib for reading remote files
# requests to download the archives, zipfile to unzip the archives
# os to delete archives when done
from tkinter import *
from tkinter import messagebox, ttk
import os, requests, sys, threading, urllib.error, urllib.request, webbrowser
from zipfile import ZipFile

# reads the local version file to get the version number,
# converts it to a float, returns result to function call
def getLocalVersion():
    try:
        open(versionFile, 'r')
    except IOError:
        actions.entryconfigure('Update Game', state=DISABLED)
        messagebox.showerror('Prelude Error', 'Local version information file cannot be found.', parent=window)
        sys.exit()
    else:
        file = open(versionFile, 'r')
        localVersion = float(file.read())
        file.close()

        return localVersion

# retrieves the remote version file to get the version number,
# converts it to a float, returns result to function call
def getRemoteVersion():
    remoteVersion = float(urllib.request.urlopen(urlPath + '/' + versionFile).read())

    return remoteVersion

# retrieves the remote message file, displays a message box if
# there are any contents, disables the menu action otherwise
def displayMessages():
    messageContents = urllib.request.urlopen(urlPath + '/' + messageFile).read()
    messageContents = messageContents.decode('UTF-8')

    if (messageContents != ''):
        messagebox.showinfo('A Message from ' + gameTitle + ' Developers', messageContents, parent=window)
    else:
        actions.entryconfigure('Display Game Developer Messages', state=DISABLED)

# checks to see how versions compare. goes through cases in order until finds a match,
# some code is executed the same way at each function call
def updateGame():
    # first case: if local core release is less than remote core release AND
    # if the remote core release is not equal to the remote patch release,
    # then download both the core and patch releases.
    if (int(localVersion) < int(remoteVersion) and int(remoteVersion) != remoteVersion):
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

    # second case: if local core release is less than remote core release AND
    # if the remote core release is equal to the remote patch release,
    # then just download the core release.
    elif (int(localVersion) < int(remoteVersion) and int(remoteVersion) == remoteVersion):
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

    # third case: if local patch release is less than the remote patch release,
    # then just download the patch release.
    elif (localVersion < remoteVersion):
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

    # fourth case: this shouldn't be happening, hence the error message.
    else:
        progressBar['value'] = 100
        progressLabel['text'] = 'Error.'

    # calls the getLocalVersion to read the new local version info,
    # sets the localVersionLabel to the new version, disables both the
    # Update Game menu option and main button
    newVersion = getLocalVersion()
    localVersionLabel['text'] = format(newVersion, '.2f')
    actions.entryconfigure('Update Game', state=DISABLED)
    updateButton['state'] = 'disabled'

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
actions.add_command(label='Display Game Developer Messages', command=displayMessages)
actions.add_separator()
actions.add_command(label='Download Latest Core', command=lambda: webbrowser.open(urlPath + '/' + coreArchive))
actions.add_command(label='Download Latest Patch', command=lambda: webbrowser.open(urlPath + '/' + patchArchive))
actions.add_separator()
actions.add_command(label='Close', command=sys.exit)
about = Menu(menubar)
menubar.add_cascade(label='About', menu=about)
about.add_command(label='About ' + gameTitle, command=lambda: webbrowser.open(gameURL))
about.add_command(label='About Prelude', command=lambda: webbrowser.open('https://gitlab.com/ariastudios/prelude'))
window.config(menu=menubar)

# checks to see if the remoote server is available, if any errors arise,
# display an error message; otherwise, proceed with main program
serverCheck = urllib.request.Request(urlPath + '/' + versionFile) # urlPath + '/' + versionFile 'http://pretend_server.org'
try:
    response = urllib.request.urlopen(serverCheck)
except urllib.error.URLError as e:
    if hasattr(e, 'reason'):
        error = str(e.reason)
        actions.entryconfigure('Update Game', state=DISABLED)
        actions.entryconfigure('Display Game Developer Messages', state=DISABLED)
        actions.entryconfigure('Close', state=DISABLED)
        messagebox.showerror('Prelude Error', 'Failed to reach the remote server. \n' + error, parent=window)
        sys.exit()
    elif hasattr(e, 'code'):
        error = str(e.code)
        actions.entryconfigure('Update Game', state=DISABLED)
        actions.entryconfigure('Display Game Developer Messages', state=DISABLED)
        actions.entryconfigure('Close', state=DISABLED)
        messagebox.showerror('Prelude Error', 'Server could not fulfill the request. \n' + error, parent=window)
        sys.exit()
else:
    # calls relevant functions for initial information
    localVersion = getLocalVersion()
    remoteVersion = getRemoteVersion()

    # displays the version information
    mainFrame = ttk.Frame(window).grid(column=0, row=0)
    versionFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(versionFrame, text='My Version:').grid(column=0, row=0, columnspan=1, rowspan=1, sticky=N, pady=10)
    localVersionLabel = ttk.Label(versionFrame, text=format(localVersion, '.2f'))
    localVersionLabel.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
    ttk.Label(versionFrame, text='Current Version:').grid(column=0, row=1, columnspan=1, rowspan=1, sticky=N, pady=10)
    ttk.Label(versionFrame, text=format(remoteVersion, '.2f')).grid(column=1, row=1, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
    ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

    # displays the progressbar, progress label, and action buttons
    updateFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
    progressBar = ttk.Progressbar(updateFrame, orient='horizontal', length=200, mode='determinate')
    progressBar.grid(column=0, row=3, columnspan=2, rowspan=1, sticky=N, pady=10)
    progressLabel = ttk.Label(updateFrame, text='Select an option below.')
    progressLabel.grid(column=0, row=4, columnspan=2, rowspan=1, sticky=N, pady=3)

    if (localVersion < remoteVersion):
        updateButton = ttk.Button(updateFrame, text='Update Game', command=lambda: threading.Thread(target=updateGame).start())
        updateButton.grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)
    else:
        updateButton = ttk.Button(updateFrame, text='Update Game', state='disabled').grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)

    closeButton = ttk.Button(updateFrame, text='Close', command=sys.exit).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)

    # displays Prelude credits
    ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=7, columnspan=2, rowspan=1)
    creditFrame = ttk.Frame(mainFrame, width=250, height=25).grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S)
    ttk.Label(creditFrame, text='Powered by Prelude v1').grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S, pady=10)

    # automatically displays any remote Messages
    displayMessages()

# creates & displays the GUI
window.mainloop()
