# to do: finalize updater updating
# to do: fix the prep section before compiling

# import relevant modules & script files
from tkinter import *
from tkinter import messagebox, ttk
import lzma, os, py7zr, requests, semantic_version, shutil, sys, threading, urllib, zipfile

import config, gui, privateBuildChannel

# checks if required variables are defined, if not display an error message and close
if (config.gameTitle == '' or config.urlPath == '' or (config.privateBuildChannelAuthMethod != '' and (config.privateBuildChannelName == '' or config.privateBuildChannelURLPath == ''))):
    messagebox.showerror('Prelude Error', 'Error: data is missing from the program configuration.\n\nContact the ' + config.gameTitle + ' developers.')
    gui.close()

if (os.path.exists('authToken') == True):
    resetToken = requests.head(config.privateBuildChannelURLPath + '/resetToken')

    if (resetToken.status_code == requests.codes.ok or config.privateBuildChannelEncKey == '' or config.privateBuildChannelAuthMethod == ''):
        os.remove('authToken')
        messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'Authorization status for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel has been reset by the ' + config.gameTitle + ' developers.\n\nYou will need to reauthorize this computer at a later date.', parent=gui.window)

# retireves the local version number, converts it to a float
def getLocalVersion(type):
    try:
        if (type == 'standard'):
            file = open('version', 'r')
        else:
            file = open(config.privateBuildChannelName + '/version', 'r')
        localVersion = semantic_version.Version(file.read())
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local version information file cannot be found. Please make sure you are running the program in the same directory as the version file (most often, your game directory).\n\nIf you are running the program in the correct location and the error persists, please contact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except ValueError:
        messagebox.showerror('Prelude Error', 'Local version information file contains invalid contents.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    file.close()

    return localVersion

# retireves the remote version number, converts it to a float
def getRemoteVersion(type):
    try:
        if (type == 'standard'):
            remoteVersion = urllib.request.urlopen(config.urlPath + '/version').read()
        else:
            remoteVersion = urllib.request.urlopen(config.privateBuildChannelURLPath + '/version').read()
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
        messagebox.showerror('Prelude Error', 'Remote version information file contains invalid contents.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    return remoteVersion

# checks to see if any messages can or should be displayed and does so,
# also enables the menu option if there are any messages that can be displayed
def displayMessages():
    if (localVersion == semantic_version.Version('0.0.0')):
        try:
            messageContent = urllib.request.urlopen(config.urlPath + '/installMessage').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s install message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo('Welcome to ' + config.gameTitle + '!', messageContent, parent=gui.window)

    if (localVersion != semantic_version.Version('0.0.0')):
        try:
            messageContent = urllib.request.urlopen(config.urlPath + '/message').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo('A Message from the ' + config.gameTitle + ' Developers', messageContent, parent=gui.window)

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
        updateType = 'standard-full'
        if (config.operatingSystem != ''):
            updateType = 'standard-full-system'
            updateAction(config.operatingSystem + '.zip', updateType)
        updateAction('core.zip', updateType)
        updateAction('patch.zip', updateType)

    # second case: if local core release is less than remote core release AND
    # if the remote core release is equal to the remote patch release,
    # then just install the core release.
    elif ((remoteVersion.major > localVersion.major or remoteVersion.minor > localVersion.minor) and remoteVersion.patch == 0):
        updateType = 'standard-core'
        if (config.operatingSystem != ''):
            updateType = 'standard-core-system'
            updateAction(config.operatingSystem + '.zip', updateType)
        updateAction('core.zip', updateType)

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
        gui.progressLabel['text'] = config.gameTitle + ' is now up to date!'
    else:
        gui.progressLabel['text'] = 'Error: version information out of sync.'
        messagebox.showerror('Prelude Error', 'Error: the local version information file is out of sync with the remote version information file.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
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
    if (os.path.exists(config.privateBuildChannelName) == True):
        privateBuildLocal = getLocalVersion('private')
    
    # create logic for update check
    if ((os.path.exists(config.privateBuildChannelName) == False and int(privateBuildRemote.prerelease[1]) > 0) or (os.path.exists(config.privateBuildChannelName) == True and privateBuildRemote.prerelease[1] > privateBuildLocal.prerelease[1])):
        if (config.privateBuildChannelAuthMethod == 'password'):
            updateExt = '.7z'
        else:
            updateExt = '.zip'

        if (int(privateBuildRemote.prerelease[1]) > 0 and (os.path.exists(config.privateBuildChannelName) == False or (os.path.exists(config.privateBuildChannelName) == True and (privateBuildRemote.major != privateBuildLocal.major or privateBuildRemote.minor != privateBuildLocal.minor)))):
            updateType = 'private-full'
            if (config.operatingSystem != ''):
                updateType = 'private-full-system'
                updateAction(config.operatingSystem + '.zip', updateType)
            updateAction('core' + updateExt, updateType)
            updateAction('patch' + updateExt, updateType)
        elif (int(privateBuildRemote.prerelease[1]) == 0 and (os.path.exists(config.privateBuildChannelName) == False or (os.path.exists(config.privateBuildChannelName) == True and (privateBuildRemote.major != privateBuildLocal.major or privateBuildRemote.minor != privateBuildLocal.minor)))):
            updateType = 'private-core'
            if (config.operatingSystem != ''):
                updateType = 'private-core-system'
                updateAction(config.operatingSystem + '.zip', updateType)
            updateAction('core' + updateExt, updateType)
        elif (privateBuildRemote.prerelease[1] > privateBuildLocal.prerelease[1]):
            updateAction('patch' + updateExt, 'private-patch')
        else:
            gui.progressBar['value'] = 100
            gui.progressLabel['text'] = 'Error.'

        newVersion = getLocalVersion('private')
        if (newVersion == privateBuildRemote):
            gui.progressLabel['text'] = 'Latest ' + config.privateBuildChannelName + ' build is now installed!'
        else:
            gui.progressLabel['text'] = 'Error: version information out of sync.'
            messagebox.showerror('Prelude Error', 'Error: the local ' + config.privateBuildChannelName + ' version information file is out of sync with the remote ' + config.privateBuildChannelName + ' version information file.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
    else:
        messagebox.showinfo(config.privateBuildChannelName + ' Build Channel', 'The latest ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel release is already installed.', parent=gui.window)

    # displays confirmation message & re-enables GUI elements
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
    gui.progressLabel['text'] = 'Preparing ' + config.gameTitle + 'game folder.'

    if (localVersion != semantic_version.Version('0.0.0') and (updateType == 'standard-full' or updateType == 'standard-core') and ((config.operatingSystem != '' and updateTarget == config.operatingSystem + '.zip') or (config.operatingSystem == '' and updateTarget == 'core.zip'))):
        retain = [os.path.basename(sys.argv[0]), 'version', 'configData', 'privateConfigData', 'misc', 'old', 'scripts', '.git', '__pycache__', '.gitignore', 'CHANGELOG.md', 'encKey', 'gui.py', 'icon.ico', 'LICENSE', 'privateBuildChannel.py', 'README.md', 'config.py', 'updater.py']

        # Loop through everything in folder in current working directory
        for item in os.listdir(os.getcwd()):
            if item not in retain:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
    elif (config.privateBuildChannelAuthMethod != '' and os.path.exists(config.privateBuildChannelName) and (updateType == 'private-full' or updateType == 'private-core') and updateTarget == 'core.zip'):
        shutil.rmtree(config.privateBuildChannelName)
        os.mkdir(config.privateBuildChannelName)

    if (os.path.exists(updateTarget) == True):
        os.remove(updateTarget)

    gui.progressBar['value'] += 5
    if (updateTarget == 'core.zip' and 'standard' in updateType):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v' + str(remoteVersion.major) + '.' + str(remoteVersion.minor) + ') archive.'
    elif (updateTarget == 'patch.zip' and 'standard' in updateType):
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' (v.' + str(remoteVersion.patch) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Downloading latest ' + updateTarget + ' archive.'

    try:
        if ('private' in updateType):
            download = requests.get(config.privateBuildChannelURLPath + '/' + updateTarget, stream=True, timeout=30)
        else:
            download = requests.get(config.urlPath + '/' + updateTarget, stream=True, timeout=30)
        download.raise_for_status()
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

    totalLength = int(download.headers.get('content-length'))
    updateFile = open(updateTarget, 'wb')

    if (totalLength > shutil.disk_usage(os.getcwd()).free):
        messagebox.showwarning('Prelude Warning', 'Warning: your hard drive may not have enough space for this download.', parent=gui.window)

    if totalLength is None:
        updateFile.write(download.content)
        if ('full-system' in updateType):
            gui.progressBar['value'] += 12
        elif ('core-system' in updateType or 'full' in updateType):
            gui.progressBar['value'] += 20
        elif ('core' in updateType or 'patch' in updateType):
            gui.progressBar['value'] += 45
    else:
        if ('full-system' in updateType):
            increment = int(totalLength / 12)
        elif ('core-system' in updateType or 'full' in updateType):
            increment = int(totalLength / 20)
        elif ('core' in updateType or 'patch' in updateType):
            increment = int(totalLength / 45)

        for data in download.iter_content(chunk_size=increment):
            updateFile.write(data)
            gui.progressBar['value'] += 1

    updateFile.close()

    if (updateTarget == 'core.zip' and 'standard' in updateType):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v' + str(remoteVersion.major) + '.' + str(remoteVersion.minor) + ') archive.'
    elif (updateTarget == 'patch.zip' and 'standard' in updateType):
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' (v.' + str(remoteVersion.patch) + ') archive.'
    else:
        gui.progressLabel['text'] = 'Extracting ' + updateTarget + ' archive.'
    
    if (py7zr.is_7zfile(updateTarget) == True):
        flag = threading.Event()
        
        if (os.path.exists('authToken') == False):
            authThread = threading.Thread(target=privateBuildChannel.createAuthWindow(updateTarget, flag))
        else:
            authThread = threading.Thread(target=privateBuildChannel.checkAuth(updateTarget, flag))

        authThread.start()
        flag.wait()
    else:
        try:
            updateFile = zipfile.ZipFile(updateTarget, 'r')
            if ('private' in updateType):
                updateFile.extractall(path=config.privateBuildChannelName)
            else:
                updateFile.extractall()
            updateFile.close()
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except zipfile.BadZipFile:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' is corrupted.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except PermissionError:
            messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' contains files currently being used by other programs or that the program cannot overwrite (including hidden files).\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()

    """ if (os.path.basename(sys.argv[0]) in updateFile.namelist()):
        messagebox.showwarning('Prelude Warning', 'Warning: this update must be manually installed. Please extract the ' + updateTarget + ' archive directly into the game directory.', parent=gui.window)
        gui.close() """

    if ('full-system' in updateType):
        gui.progressBar['value'] += 12
    elif ('core-system' in updateType or 'full' in updateType):
        gui.progressBar['value'] += 20
    elif ('core' in updateType or 'patch' in updateType):
        gui.progressBar['value'] += 45
    gui.progressLabel['text'] = 'Deleting ' + updateTarget + ' archive.'

    try:
        os.remove(updateTarget)
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local archive ' + updateTarget + ' cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()

    gui.progressBar['value'] += 5

# sets the relevant GUI item commands
standardThread = threading.Thread(target=standardBuild)
gui.actions.entryconfigure('Update Game', command=lambda: standardThread.start())
gui.actions.entryconfigure('Display Game Developer Messages', command=displayMessages)
gui.updateButton['command'] = lambda: standardThread.start()
if (config.privateBuildChannelAuthMethod != ''):
    gui.privateBuildChannel.entryconfigure('Display ' + config.privateBuildChannelName + ' Build Messages', command=lambda: privateBuildChannel.messages())
    privateThread = threading.Thread(target=privateBuild)
    gui.privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build', command=lambda: privateThread.start())

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
if (config.privateBuildChannelAuthMethod != ''):
    gui.privateBuildChannel.entryconfigure('Install Latest ' + config.privateBuildChannelName + ' Build', state=NORMAL)

# displays any messages, checks if the computer is
# authorized for the private build channel
displayMessages()
if (config.privateBuildChannelAuthMethod != ''):
    privateBuildChannel.messages()

# creates & displays the GUI
gui.window.mainloop()