# to do: fix private build pipeline (new folder, deleting old install, etc.)
# to do: fix progress bar/GUI messages
# to do: finalize updater updating

# import relevant modules & script files
from tkinter import *
from tkinter import messagebox, ttk
import lzma, os, py7zr, requests, semantic_version, shutil, sys, threading, urllib, zipfile

import setup, gui, privateBuildChannel

# checks if required variables are defined, if not display an error message and close
if (setup.gameTitle == '' or setup.urlPath == '' or (setup.privateBuildChannelAuthMethod != '' and (setup.privateBuildChannelName == '' or setup.privateBuildChannelURLPath == ''))):
    messagebox.showerror('Prelude Error', 'Error: data is missing from the program configuration.\n\nContact the ' + setup.gameTitle + ' developers.')
    gui.close()

# retireves the local version number, converts it to a float
def getLocalVersion(type):
    try:
        if (type == 'standard'):
            file = open('version', 'r')
        else:
            file = open(setup.privateBuildChannelName + '/version', 'r')
        localVersion = semantic_version.Version(file.read())
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local version information file cannot be found. Please make sure you are running the program in the same directory as the version file (most often, your game directory).\n\nIf you are running the program in the correct location and the error persists, please contact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except ValueError:
        messagebox.showerror('Prelude Error', 'Local version information file contains invalid contents.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    file.close()

    return localVersion

# retireves the remote version number, converts it to a float
def getRemoteVersion(type):
    try:
        if (type == 'standard'):
            remoteVersion = urllib.request.urlopen(setup.urlPath + '/version').read()
        else:
            remoteVersion = urllib.request.urlopen(setup.privateBuildChannelURLPath + '/version').read()
        remoteVersion = remoteVersion.decode('UTF-8')
        remoteVersion = semantic_version.Version(remoteVersion)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s version information file.\n\n' + str(e.reason), parent=gui.window)
            gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
            gui.close()
    except ValueError:
        messagebox.showerror('Prelude Error', 'Remote version information file contains invalid contents.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    return remoteVersion

# checks to see if any messages can or should be displayed and does so,
# also enables the menu option if there are any messages that can be displayed
def displayMessages():
    if (localVersion == semantic_version.Version('0.0.0')):
        try:
            messageContent = urllib.request.urlopen(setup.urlPath + '/installMessage').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s install message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo('Welcome to ' + setup.gameTitle + '!', messageContent, parent=gui.window)

    if (localVersion != semantic_version.Version('0.0.0')):
        try:
            messageContent = urllib.request.urlopen(setup.urlPath + '/message').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo('A Message from the ' + setup.gameTitle + ' Developers', messageContent, parent=gui.window)

    if (setup.privateBuildChannelAuthMethod != ''):
        privateBuildChannel.messages()
    
    gui.actions.entryconfigure('Display Game Developer Messages', state=NORMAL)

# logic tree to determine what gets updated for the regular release channel
def standardBuild():
    # disables the GUI elements
    gui.disable()
    if (localVersion == semantic_version.Version('0.0.0')):
        gui.actions.entryconfigure('Install Game', state=DISABLED)
    else:
        gui.actions.entryconfigure('Update Game', state=DISABLED)
    gui.progressBar['value'] = 0

    # first case: if local core release is less than remote core release AND
    # if the remote core release is not equal to the remote patch release,
    # then install both the core and patch releases.
    if ((remoteVersion.major > localVersion.major or remoteVersion.minor > localVersion.minor) and remoteVersion.patch > 0):
        if (setup.operatingSystem != ''):
            updateAction(setup.operatingSystem + '.zip', 'standard-full')
        updateAction('core.zip', 'standard-full')
        updateAction('patch.zip', 'standard-full')

    # second case: if local core release is less than remote core release AND
    # if the remote core release is equal to the remote patch release,
    # then just install the core release.
    elif ((remoteVersion.major > localVersion.major or remoteVersion.minor > localVersion.minor) and remoteVersion.patch == 0):
        if (setup.operatingSystem != ''):
            updateAction(setup.operatingSystem + '.zip', 'standard-core')
        updateAction('core.zip', 'standard-core')

    # third case: if local patch release is less than the remote patch release,
    # then just install the patch release.
    elif ((remoteVersion.major == localVersion.major and remoteVersion.minor == localVersion.minor) and remoteVersion.patch > localVersion.patch):
        updateAction('patch.zip', 'standard-patch')

    # fourth case: this shouldn't be happening, hence the error message.
    else:
        gui.progressBar['value'] = 100
        gui.progressLabel['text'] = 'Error.'

    # checks if the new local version is correct, displays message based on that
    # re-enables GUI elements
    newVersion = getLocalVersion('standard')
    gui.localVersionLabel['text'] = newVersion
    if (newVersion == remoteVersion):
        gui.progressLabel['text'] = setup.gameTitle + ' is now up to date!'
    else:
        gui.progressLabel['text'] = 'Error: version information out of sync.'
        messagebox.showerror('Prelude Error', 'Error: the local version information file is out of sync with the remote version information file.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
    gui.enable()
    gui.updateButton['state'] = 'disabled'

# installs the latest private build channel core release
def privateBuild():
    # disables GUI elements
    gui.disable()
    if (localVersion == semantic_version.Version('0.0.0')):
        gui.actions.entryconfigure('Install Game', state=DISABLED)
    else:
        gui.actions.entryconfigure('Update Game', state=DISABLED)
    gui.progressBar['value'] = 0


    privateBuildRemote = getRemoteVersion('private')
    if (os.path.exists(setup.privateBuildChannelName) == True):
        privateBuildLocal = getLocalVersion('private')

    if (int(privateBuildRemote.prerelease[1]) > 0 and (os.path.exists(setup.privateBuildChannelName) == False or (os.path.exists(setup.privateBuildChannelName) == True and (privateBuildRemote.major != privateBuildLocal.major or privateBuildRemote.minor != privateBuildLocal.minor)))):
        if (setup.operatingSystem != ''):
            updateAction(setup.operatingSystem + '.zip', 'private-full')
        if (setup.privateBuildChannelAuthMethod == 'none'):
            updateAction('core.zip', 'private-full')
            updateAction('patch.zip', 'private-full')
        elif (setup.privateBuildChannelAuthMethod == 'password'):
            updateAction('core.7z', 'private-full')
            updateAction('patch.7z', 'private-full')
    elif (int(privateBuildRemote.prerelease[1]) == 0 and (os.path.exists(setup.privateBuildChannelName) == False or (os.path.exists(setup.privateBuildChannelName) == True and (privateBuildRemote.major != privateBuildLocal.major or privateBuildRemote.minor != privateBuildLocal.minor)))):
        if (setup.operatingSystem != ''):
            updateAction(setup.operatingSystem + '.zip', 'private-core')
        if (setup.privateBuildChannelAuthMethod == 'none'):
            updateAction('core.zip', 'private-core')
        elif (setup.privateBuildChannelAuthMethod == 'password'):
            updateAction('core.7z', 'private-core')
    elif (privateBuildRemote.prerelease[1] > privateBuildLocal.prerelease[1]):
        if (setup.privateBuildChannelAuthMethod == 'none'):
            updateAction('patch.zip', 'private-patch')
        elif (setup.privateBuildChannelAuthMethod == 'password'):
            updateAction('patch.7z', 'private-patch')
    else:
        print('logical error.')

    # displays confirmation message & re-enables GUI elements
    gui.progressLabel['text'] = 'Latest ' + setup.privateBuildChannelName + ' build is now installed!'
    gui.enable()
    if (localVersion != remoteVersion):
        if (localVersion == semantic_version.Version('0.0.0')):
            gui.actions.entryconfigure('Install Game', state=NORMAL)
        else:
            gui.actions.entryconfigure('Update Game', state=NORMAL)
    else:
        gui.updateButton['state'] = 'disabled'

# handles the actual updating, based on the targetted archive and what kind of update it is
# also updates the progress bar and label depending on the same
def updateAction(updateTarget, updateType):
    if (localVersion != semantic_version.Version('0.0.0') and (updateType == 'standard-full' or updateType == 'standard-core') and ((setup.operatingSystem != '' and updateTarget == setup.operatingSystem + '.zip') or (setup.operatingSystem == '' and updateTarget == 'core.zip'))):
        retain = [os.path.basename(sys.argv[0]), 'version', 'configData', 'privateConfigData', 'misc', 'old', 'scripts', '.git', '__pycache__', '.gitignore', 'CHANGELOG.md', 'encKey', 'gui.py', 'icon.ico', 'LICENSE', 'privateBuildChannel.py', 'README.md', 'setup.py', 'updater.py']

        # Loop through everything in folder in current working directory
        for item in os.listdir(os.getcwd()):
            if item not in retain:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
    elif (setup.privateBuildChannelAuthMethod != '' and os.path.exists(setup.privateBuildChannelName) and (updateType == 'private-full' or updateType == 'private-core') and updateTarget == 'core.zip'):
        shutil.rmtree(setup.privateBuildChannelName)
        os.mkdir(setup.privateBuildChannelName)

    if (updateTarget == 'core.zip'):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(remoteVersion.major) + '.' + str(remoteVersion.minor) + ') archive.'
    elif (updateTarget == 'patch.zip'):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v.' + str(remoteVersion.patch) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' archive.'

    if (os.path.exists(updateTarget) == True):
        os.remove(updateTarget)

    try:
        if (updateType == 'private-full' or updateType == 'private-core' or updateType == 'private-patch'):
            download = requests.get(setup.privateBuildChannelURLPath + '/' + updateTarget, stream=True, timeout=30)
        else:
            download = requests.get(setup.urlPath + '/' + updateTarget, stream=True, timeout=30)
        download.raise_for_status()
    except requests.exceptions.HTTPError as error:
        messagebox.showerror('Prelude Error', 'HTTP error: #' + str(error) + '.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Prelude Error', 'Connection error. \n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.TooManyRedirects:
        messagebox.showerror('Prelude Error', 'Server connection exceeded maximum number of redirects.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.Timeout:
        messagebox.showerror('Prelude Error', 'Server connection timed out, try again later.', parent=gui.window)
        gui.close()
    except requests.exceptions.RequestException as error:
        messagebox.showerror('Prelude Error', 'Error: ' + str(error) + '.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    totalLength = int(download.headers.get('content-length'))
    updateFile = open(updateTarget, 'wb')

    if (totalLength > shutil.disk_usage(os.getcwd()).free):
        messagebox.showwarning('Prelude Warning', 'Warning: your hard drive may not have enough space for this download.', parent=gui.window)

    if totalLength is None:
        updateFile.write(download.content)
        if (updateType == 'full'):
            gui.progressBar['value'] += 40
        else:
            gui.progressBar['value'] += 90
    else:
        if (updateType == 'full'):
            increment = int(totalLength / 40)
        else:
            increment = int(totalLength / 90)

        for data in download.iter_content(chunk_size=increment):
            updateFile.write(data)
            gui.progressBar['value'] += 1

    updateFile.close()

    if (updateTarget == 'core.zip'):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(remoteVersion.major) + '.' + str(remoteVersion.minor) + ') archive.'
    elif (updateTarget == 'patch.zip'):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v.' + str(remoteVersion.patch) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' archive.'
    
    if (py7zr.is_7zfile(updateTarget) == True):
        print('somehow make this actually work.')
        
        # privThread = threading.Thread(target=privateBuildChannel.testPassword(updateTarget))
        # privThread.start()
    else:
        try:
            updateFile = zipfile.ZipFile(updateTarget, 'r')
            if (updateType == 'private-full' or updateType == 'private-core' or updateType == 'private-patch'):
                updateFile.extractall(path=setup.privateBuildChannelName)
            else:
                updateFile.extractall()
            updateFile.close()
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except zipfile.BadZipFile:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' is corrupted.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except PermissionError:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' contains files currently being used by other programs or that the program cannot overwrite (including hidden files).\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
            gui.close()

    """ if (os.path.basename(sys.argv[0]) in updateFile.namelist()):
        messagebox.showwarning('Prelude Warning', 'Warning: this update must be manually installed. Please extract the ' + updateTarget + ' archive directly into the game directory.', parent=gui.window)
        gui.close() """

    gui.progressBar['value'] += 5

    if (updateTarget == 'core.zip'):
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v' + str(remoteVersion.major) + '.' + str(remoteVersion.minor) + ') archive.'
    elif (updateTarget == 'patch.zip'):
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' (v.' + str(remoteVersion.patch) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' archive.'

    try:
        os.remove(updateTarget)
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    gui.progressBar['value'] += 5

# sets the relevant GUI item commands
gui.actions.entryconfigure('Update Game', command=lambda: threading.Thread(target=standardBuild).start())
gui.actions.entryconfigure('Display Game Developer Messages', command=displayMessages)
gui.updateButton['command'] = lambda: threading.Thread(target=standardBuild).start()
if (setup.privateBuildChannelAuthMethod != ''):
    gui.privateBuildChannel.entryconfigure('Authorization', command=None)
    threadTest = threading.Thread(target=privateBuild)
    gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', command=lambda: threadTest.start())

# call relevant functions to get version information,
# set the appropriate labels to the returned information
# if the local version is out of date, enable the update options
localVersion = getLocalVersion('standard')
remoteVersion = getRemoteVersion('standard')
gui.localVersionLabel['text'] = localVersion
gui.remoteVersionLabel['text'] = remoteVersion
if (localVersion == semantic_version.Version('0.0.0') and remoteVersion > semantic_version.Version('0.0.0')):
    gui.actions.entryconfigure('Update Game', label='Install Game', state=NORMAL)
    gui.updateButton['text'] = 'Install Game'
    gui.updateButton['state'] = NORMAL
elif (remoteVersion > localVersion):
    gui.actions.entryconfigure('Update Game', state=NORMAL)
    gui.updateButton['state'] = NORMAL

# displays any messages, checks if the computer is
# authorized for the private build channel
privateBuildChannel.checkStatus()
displayMessages()
gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', state=NORMAL)

# creates & displays the GUI
gui.window.mainloop()