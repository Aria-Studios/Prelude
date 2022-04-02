# import relevant modules
# tkinter for GUI, webbrowser to launch menu links
# threading for progressbar, urllib for reading remote files
# requests to download the archives, zipfile to unzip the archives
# os to delete archives when done
from tkinter import *
from tkinter import messagebox, ttk
import os, requests, shutil, sys, threading, urllib, zipfile

import config, gui, authorization

# checks if required variables are defined, if not display an error message and close
if (config.urlPath == '' or config.versionFile == '' or config.coreArchive == '' or config.patchArchive == ''):
    messagebox.showerror('Prelude Error', 'Error: data is missing from the program configuration.\n\nContact the ' + config.gameTitle + ' developers.')
    gui.close()

# passes the versionFile to local error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getLocalVersion():
    try:
        file = open(config.versionFile, 'r')
        localVersion = float(file.read())
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local ' + config.versionFile + ' information file cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except ValueError:
        messagebox.showerror('Prelude Error', 'Local ' + config.versionFile + ' information file contains invalid contents.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    file.close()

    return localVersion

# passes the versionFile to remote error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getRemoteVersion():
    try:
        remoteVersion = float(urllib.request.urlopen(config.urlPath + '/' + config.versionFile).read())
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.versionFile + ' information file.\n\n' + str(e.reason), parent=gui.window)
            gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
            gui.close()
    except ValueError:
        messagebox.showerror('Prelude Error', 'Remote ' + config.versionFile + ' information file contains invalid contents.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    return remoteVersion

# passes the messageFile to remote error handling, if no errors are
# found then it retireves the message contents, converts it
# to a string, displays the contents in a message box and enables the menu action
# (if there are any, otherwise it disables the menu action [again])
def displayMessages():
    if (localVersion == 0 and config.installMessage != ''):
        messagebox.showinfo('A Message from the ' + config.gameTitle + ' Developers', config.installMessage, parent=gui.window)

    if (localVersion != 0 and config.messageFile != ''):
        try:
            messageContents = urllib.request.urlopen(config.urlPath + '/' + config.messageFile).read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.messageFile + ' information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)

        messageContents = messageContents.decode('UTF-8')

        if (messageContents != ''):
            messagebox.showinfo('A Message from the ' + config.gameTitle + ' Developers', messageContents, parent=gui.window)

    if (config.messageFile != ''):
        gui.actions.entryconfigure('Display Game Developer Messages', command=displayMessages, state=NORMAL)

# logic tree to determine what gets updated
def updateGame():
    # disables the update menu item & button, as well as the message menu item
    if (localVersion == 0):
        gui.actions.entryconfigure('Install Game', state=DISABLED)
    else:
        gui.actions.entryconfigure('Update Game', state=DISABLED)
    gui.actions.entryconfigure('Display Game Developer Messages', state=DISABLED)
    gui.updateButton['state'] = 'disabled'

    messagebox.showwarning('Prelude Warning', 'This program is still in development and will not reflect the status of your download. Please give it time to work. You can check your task manager to see if it is still processing the download (check the RAM usage) if necessary.', parent=gui.window)

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
        messagebox.showerror('Prelude Error', 'Error: the local version information file is out of sync with the remote version information file.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
    gui.actions.entryconfigure('Display Game Developer Messages', state=NORMAL)

# handles the actual updating, based on the targetted archive and what kind of update it is
# also updates the progress bar and label depending on the same
def updateAction(updateTarget, updateType):
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    if (shutil.disk_usage(os.getcwd()).free < int(requests.head(config.urlPath + '/' + updateTarget).headers['Content-length'])):
        messagebox.showwarning('Prelude Warning', 'Warning: your hard drive may not have enough space for this download.', parent=gui.window)

    try:
        updateZip = requests.get(config.urlPath + '/' + updateTarget, timeout=30)
        updateZip.raise_for_status()
    except requests.exceptions.HTTPError as error:
        messagebox.showerror('Prelude Error', 'HTTP error: #' + str(error) + '.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Prelude Error', 'Connection error. \n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.TooManyRedirects:
        messagebox.showerror('Prelude Error', 'Server connection exceeded maximum number of redirects.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.Timeout:
        messagebox.showerror('Prelude Error', 'Server connection timed out, try again later.', parent=gui.window)
        gui.close()
    except requests.exceptions.RequestException as error:
        messagebox.showerror('Prelude Error', 'Error: ' + str(error) + '.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    updateFile = open(updateTarget, 'wb')
    updateFile.write(updateZip.content)
    updateFile.close()

    gui.updatePBar(updateType)
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    try:
        updateFile = zipfile.ZipFile(updateTarget, 'r')
        updateFile.extractall()
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except zipfile.BadZipFile:
        messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' is corrupted.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except PermissionError:
        if (os.path.basename(sys.argv[0]) in updateTarget.namelist()):
            messagebox.showwarning('Prelude Warning', 'Warning: this update must be manually installed. Please extract the ' + updateTarget + ' archive directly into the game directory.', parent=gui.window)
            gui.close()
        else:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' contains files currently being used by other programs.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()

    updateFile.close()

    gui.updatePBar(updateType)
    if (updateTarget == config.coreArchive):
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v' + str(int(remoteVersion)) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v' + str(float(remoteVersion)) + ') archive.'

    try:
        os.remove(updateTarget)
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    gui.updatePBar(updateType)

# call relevant functions to get version information,
# set the appropriate labels to the returned information
localVersion = getLocalVersion()
remoteVersion = getRemoteVersion()
gui.localVersionLabel['text'] = localVersion
gui.remoteVersionLabel['text'] = remoteVersion
displayMessages()

if (config.authMethod == 'none'):
    gui.privateBuildChannel.entryconfigure('Install ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)
    gui.privateBuildChannel.entryconfigure('Update ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)
elif (config.authMethod == 'password'):
    if (os.path.exists(config.tokenFile) == True):
        authorization.checkStatus()
    else:
        gui.privateBuildChannel.entryconfigure('Authorization', command=lambda: threading.Thread(target=authorization.createAuthWindow).start(), state=NORMAL)
else:
    gui.menubar.entryconfigure(config.privateBuildChannelName + ' Build Channel', state='disabled')

# if the local version is out of date, enable the update options
if (localVersion == 0):
    gui.actions.entryconfigure('Update Game', label='Install Game', command=lambda: threading.Thread(target=updateGame).start(), state=NORMAL)
    gui.updateButton['text'] = 'Install Game'
    gui.updateButton['command'] = lambda: threading.Thread(target=updateGame).start()
    gui.updateButton['state'] = NORMAL
elif (localVersion < remoteVersion):
    gui.actions.entryconfigure('Update Game', command=lambda: threading.Thread(target=updateGame).start(), state=NORMAL)
    gui.updateButton['command'] = lambda: threading.Thread(target=updateGame).start()
    gui.updateButton['state'] = NORMAL

# creates & displays the GUI
gui.window.mainloop()
