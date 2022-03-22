# import relevant modules
# tkinter for GUI, webbrowser to launch menu links
# threading for progressbar, urllib for reading remote files
# requests to download the archives, zipfile to unzip the archives
# os to delete archives when done
from tkinter import *
from tkinter import messagebox, ttk
import os, requests, shutil, threading, urllib, zipfile

import config, gui, errorHandling

# checks if required variables are defined, if not display an error message and close
if (config.urlPath == '' or config.versionFile == '' or config.coreArchive == '' or config.patchArchive == ''):
    messagebox.showerror('Prelude Error', 'Error: data is missing from the program configuration.\nContact the ' + config.gameTitle + ' developers.')
    gui.close()

# passes the versionFile to local error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getLocalVersion():
    if (errorHandling.localCheck(config.versionFile) == False):
        file = open(config.versionFile, 'r')
        localVersion = float(file.read())
        file.close()
        return localVersion

# passes the versionFile to remote error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getRemoteVersion():
    if (errorHandling.remoteCheck(config.versionFile) == False):
        remoteVersion = float(urllib.request.urlopen(config.urlPath + '/' + config.versionFile).read())
        return remoteVersion

# passes the messageFile to remote error handling, if no errors are
# found then it retireves the message contents, converts it
# to a string, displays the contents in a message box and enables the menu action
# (if there are any, otherwise it disables the menu action [again])
def displayMessages():
    if (config.messageFile != ''):
        if (errorHandling.remoteCheck(config.messageFile) == False):
            messageContents = urllib.request.urlopen(config.urlPath + '/' + config.messageFile).read()
            messageContents = messageContents.decode('UTF-8')

            if (messageContents != ''):
                messagebox.showinfo('A Message from the ' + config.gameTitle + ' Developers', messageContents, parent=gui.window)


# logic tree to determine what gets updated
def updateGame():
    # disables the update menu item & button, as well as the message menu item
    gui.actions.entryconfigure('Update Game', state=DISABLED)
    gui.actions.entryconfigure('Display Game Developer Messages', state=DISABLED)
    gui.updateButton['state'] = 'disabled'

    # first case: if local core release is less than remote core release AND
    # if the remote core release is not equal to the remote patch release,
    # then install both the core and patch releases.
    if (int(localVersion) < int(remoteVersion) and int(remoteVersion) != remoteVersion):
        updateAction(config.coreArchive, 'both')
        updateAction(config.patchArchive, 'both')

    # second case: if local core release is less than remote core release AND
    # if the remote core release is equal to the remote patch release,
    # then just install the core release.
    elif (int(localVersion) < int(remoteVersion) and int(remoteVersion) == remoteVersion):
        updateAction(config.coreArchive, 'core')

    # third case: if local patch release is less than the remote patch release,
    # then just install the patch release.
    elif (localVersion < remoteVersion):
        updateAction(config.patchArchive, 'patch')

    # fourth case: this shouldn't be happening, hence the error message.
    else:
        gui.progressBar['value'] = 100
        gui.progressLabel['text'] = 'Error.'

    # calls the getLocalVersion to read the new local version info,
    # sets the localVersionLabel to the new version, displays a update confirmation
    # message, and re-enables the messages menu item
    newVersion = getLocalVersion()
    gui.localVersionLabel['text'] = newVersion
    if (newVersion == remoteVersion):
        gui.progressLabel['text'] = config.gameTitle + ' is now up to date!'
    else:
        gui.progressLabel['text'] = 'Error: version information out of sync.'
        messagebox.showerror('Prelude Error', 'Error: the local version information file is out of sync with the remote version information file.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
    gui.actions.entryconfigure('Display Game Developer Messages', state=NORMAL)

# handles the actual updating, based on the targetted archive and what kind of update it is
# also updates the progress bar and label depending on the same
def updateAction(updateTarget, updateType):
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    if (errorHandling.downloadCheck(updateTarget) == False):
        if (shutil.disk_usage(os.getcwd()).free < int(requests.head(config.urlPath + '/' + updateTarget).headers['Content-length'])):
            messagebox.showwarning('Prelude Warning', 'Warning: your hard drive may not have enough space for this download.', parent=gui.window)
        updateZip = requests.get(config.urlPath + '/' + updateTarget, timeout=30)
        updateFile = open(updateTarget, 'wb')
        updateFile.write(updateZip.content)
        updateFile.close()

    gui.updatePBar(updateType)
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    if (errorHandling.localCheck(updateTarget) == False):
        updateFile = zipfile.ZipFile(updateTarget, 'r')
        updateFile.extractall()
        updateFile.close()

    gui.updatePBar(updateType)
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    if (errorHandling.localCheck(updateTarget) == False):
        os.remove(updateTarget)

    gui.updatePBar(updateType)

# call relevant functions to get version information,
# set the appropriate labels to the returned information
localVersion = getLocalVersion()
remoteVersion = getRemoteVersion()
gui.localVersionLabel['text'] = localVersion
gui.remoteVersionLabel['text'] = remoteVersion

# display any remote messages
if (config.messageFile != ''):
    displayMessages()
    gui.actions.entryconfigure('Display Game Developer Messages', command=displayMessages, state=NORMAL)

# if the local version is out of date, enable the update options
if (localVersion < remoteVersion):
    gui.actions.entryconfigure('Update Game', command=lambda: threading.Thread(target=updateGame).start(), state=NORMAL)
    gui.updateButton['command'] = lambda: threading.Thread(target=updateGame).start()
    gui.updateButton['state'] = NORMAL

# creates & displays the GUI
gui.window.mainloop()
