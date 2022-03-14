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

# passes the versionFile to local error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getLocalVersion():
    if (localErrorCheck(versionFile) == False):
        file = open(versionFile, 'r')
        localVersion = float(file.read())
        file.close()
        return localVersion

# passes the versionFile to remote error handling, if no errors are
# found then it retireves the version number, converts it
# to a float, and returns the result to the function call
def getRemoteVersion():
    if (remoteErrorCheck(versionFile) == False):
        remoteVersion = float(urllib.request.urlopen(urlPath + '/' + versionFile).read())
        return remoteVersion

# passes the messageFile to remote error handling, if no errors are
# found then it retireves the message contents, converts it
# to a string, displays the contents in a message box and enables the menu action
# (if there are any, otherwise it disables the menu action)
def displayMessages():
    if (remoteErrorCheck(messageFile) == False):
        messageContents = urllib.request.urlopen(urlPath + '/' + messageFile).read()
        messageContents = messageContents.decode('UTF-8')

        if (messageContents != ''):
            messagebox.showinfo('A Message from ' + gameTitle + ' Developers', messageContents, parent=window)
            actions.entryconfigure('Display Game Developer Messages', state=NORMAL)
        else:
            actions.entryconfigure('Display Game Developer Messages', state=DISABLED)

# checks to see how versions compare. goes through cases in order until finds a match,
# some code is executed the same way at each function call. all pieces are passed to
# the relevant error handling function
def updateGame():
    # first case: if local core release is less than remote core release AND
    # if the remote core release is not equal to the remote patch release,
    # then install both the core and patch releases.
    if (int(localVersion) < int(remoteVersion) and int(remoteVersion) != remoteVersion):
        progressLabel['text'] = 'Downloading latest core (' + str(remoteVersion) + ') archive.'

        if (downloadErrorCheck(coreArchive) == False):
            coreZip = requests.get(urlPath + '/' + coreArchive, timeout=30)
            coreFile = open(coreArchive, 'wb')
            coreFile.write(coreZip.content)
            coreFile.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Extracting core (' + str(remoteVersion) + ') archive.'

        if (localErrorCheck(coreArchive) == False):
            coreFile = ZipFile(coreArchive, 'r')
            coreFile.extractall()
            coreFile.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Deleting core (' + str(remoteVersion) + ') archive.'

        os.remove(coreArchive)

        progressBar['value'] += 10
        progressLabel['text'] = 'Downloading latest patch (' + str(remoteVersion) + ') archive.'

        if (downloadErrorCheck(patchArchive) == False):
            patchZip = requests.get(urlPath + '/' + patchArchive, timeout=30)
            patchFile = open(patchArchive, 'wb')
            patchFile.write(patchZip.content)
            patchFile.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Extracting patch (' + str(remoteVersion) + ') archive.'

        if (localErrorCheck(patchArchive) == False):
            patchFile = ZipFile(patchArchive, 'r')
            patchFile.extractall()
            patchFile.close()

        progressBar['value'] += 20
        progressLabel['text'] = 'Deleting patch (' + str(remoteVersion) + ') archive.'

        os.remove(patchArchive)

        progressBar['value'] += 10
        progressLabel['text'] = gameTitle + ' is now up to date!'

    # second case: if local core release is less than remote core release AND
    # if the remote core release is equal to the remote patch release,
    # then just install the core release.
    elif (int(localVersion) < int(remoteVersion) and int(remoteVersion) == remoteVersion):
        progressLabel['text'] = 'Downloading latest core (' + str(remoteVersion) + ') archive.'

        if (downloadErrorCheck(coreArchive) == False):
            coreZip = requests.get(urlPath + '/' + coreArchive, timeout=30)
            coreFile = open(coreArchive, 'wb')
            coreFile.write(coreZip.content)
            coreFile.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Extracting core (' + str(remoteVersion) + ') archive.'

        if (localErrorCheck(coreArchive) == False):
            coreFile = ZipFile(coreArchive, 'r')
            coreFile.extractall()
            coreFile.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Deleting core (' + str(remoteVersion) + ') archive.'

        os.remove(coreArchive)

        progressBar['value'] += 20
        progressLabel['text'] = gameTitle + ' is now up to date!'

    # third case: if local patch release is less than the remote patch release,
    # then just install the patch release.
    elif (localVersion < remoteVersion):
        progressLabel['text'] = 'Downloading latest patch (' + str(remoteVersion) + ') archive.'

        if (downloadErrorCheck(patchArchive) == False):
            patchZip = requests.get(urlPath + '/' + patchArchive, timeout=30)
            patchFile = open(patchArchive, 'wb')
            patchFile.write(patchZip.content)
            patchFile.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Extracting patch (' + str(remoteVersion) + ') archive.'

        if (localErrorCheck(patchArchive) == False):
            patchFile = ZipFile(patchArchive, 'r')
            patchFile.extractall()
            patchFile.close()

        progressBar['value'] += 40
        progressLabel['text'] = 'Deleting patch (' + str(remoteVersion) + ') archive.'

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

# Error handling for checking to see if local files exist
def localErrorCheck(fileToCheck):
    if (fileToCheck == 'version'):
        try:
            open(fileToCheck)
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local ' + fileToCheck + ' information file cannot be found.', parent=window)
            sys.exit()
        else:
            return False
    else:
        try:
            ZipFile(fileToCheck)
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local archive cannot be found.', parent=window)
            sys.exit()
        else:
            return False

# Error handling for checking to see if remote files can be reached
def remoteErrorCheck(fileToCheck):
    try:
        urllib.request.urlopen(urlPath + '/' + fileToCheck).read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + fileToCheck + ' information file.\n' + str(e.reason), parent=window)
            if (fileToCheck == 'version'):
                sys.exit()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n' + str(e.code), parent=window)
            if (fileToCheck == 'version'):
                sys.exit()
    else:
        return False

# Error handling for downloading zip archives
def downloadErrorCheck(fileToCheck):
    try:
        dl = requests.get(urlPath + '/' + fileToCheck, timeout=30)
        dl.raise_for_status()
    except requests.exceptions.HTTPError as error:
        messagebox.showerror('Prelude Error', 'HTTP error: ' + str(error) + '.\nContact ' + gameTitle + ' developers.', parent=window)
        sys.exit()
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Prelude Error', 'Connection error. \nContact ' + gameTitle + ' developers.', parent=window)
        sys.exit()
    except requests.exceptions.TooManyRedirects:
        messagebox.showerror('Prelude Error', 'Server connection exceeded maximum number of redirects.\nContact ' + gameTitle + ' developers.', parent=window)
        sys.exit()
    except requests.exceptions.Timeout:
        messagebox.showerror('Prelude Error', 'Server connection timed out, try again later.', parent=window)
        sys.exit()
    except requests.exceptions.RequestException as error:
        messagebox.showerror('Prelude Error', 'Error: ' + str(error) + '.\nContact ' + gameTitle + ' developers.', parent=window)
        sys.exit()
    else:
        return False

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
actions.add_command(label='Update Game', command=lambda: threading.Thread(target=updateGame).start(), state='disabled')
actions.add_command(label='Display Game Developer Messages', command=displayMessages, state='disabled')
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

# displays the version information
mainFrame = ttk.Frame(window).grid(column=0, row=0)
versionFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
ttk.Label(versionFrame, text='My Version:').grid(column=0, row=0, columnspan=1, rowspan=1, sticky=N, pady=10)
localVersionLabel = ttk.Label(versionFrame, text=format(0, '.2f'))
localVersionLabel.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Label(versionFrame, text='Current Version:').grid(column=0, row=1, columnspan=1, rowspan=1, sticky=N, pady=10)
remoteVersionLabel = ttk.Label(versionFrame, text=format(0, '.2f'))
remoteVersionLabel.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=N, padx=50, pady=10)
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

# displays the progressbar, progress label, and action buttons
updateFrame = ttk.Frame(mainFrame, width=250, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
progressBar = ttk.Progressbar(updateFrame, orient='horizontal', length=200, mode='determinate')
progressBar.grid(column=0, row=3, columnspan=2, rowspan=1, sticky=N, pady=10)
progressLabel = ttk.Label(updateFrame, text='Select an option below.')
progressLabel.grid(column=0, row=4, columnspan=2, rowspan=1, sticky=N, pady=3)
updateButton = ttk.Button(updateFrame, text='Update Game', command=lambda: threading.Thread(target=updateGame).start(), state='disabled')
updateButton.grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N, pady=10)
closeButton = ttk.Button(updateFrame, text='Close', command=sys.exit).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)

# displays Prelude credits
ttk.Separator(mainFrame, orient='horizontal').grid(column=0, row=7, columnspan=2, rowspan=1)
creditFrame = ttk.Frame(mainFrame, width=250, height=25).grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S)
ttk.Label(creditFrame, text='Powered by Prelude v1').grid(column=0, row=8, columnspan=2, rowspan=1, sticky=S, pady=10)

# call relevant functions to get version information,
# set the appropriate labels to the returned information
localVersion = getLocalVersion()
remoteVersion = getRemoteVersion()
localVersionLabel['text'] = format(localVersion, '.2f')
remoteVersionLabel['text'] = format(remoteVersion, '.2f')

# display any remote messages
displayMessages()

# if the local version is out of date, enable the update options
if (localVersion < remoteVersion):
    actions.entryconfigure('Update Game', state=NORMAL)
    updateButton['state'] = NORMAL

# creates & displays the GUI
window.mainloop()
